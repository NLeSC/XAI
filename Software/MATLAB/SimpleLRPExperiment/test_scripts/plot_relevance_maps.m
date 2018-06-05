% plot_relevance_maps - script to visualize relevance maps

%% parameters
config_params_tri_sq_rot;
verbose = true;
%normalize = input('Normalize relevance maps [1=true|0=false]?: ');
normalize = false;
%subplots = input('Use subplots [1=true|0=false]?: ');
subplots = true;
%titles = input('Use titles [1=true|0=false]?: ');
titles = true;

% select 2 images of the 2 shapes who are correctly classified
if binary
    indecies_sq = [1 8 31 798 6969 10685 16628 18764 22161 29998];
    indecies_tri  = [4 9 32 799 6970 10686 16629 18765 22162 29999];
else
    indecies_sq = [2 66 6734 9749 17495 19954 21855 22801 26519 29995];
    indecies_tri  = indecies_sq +1;

end
num_shape_pairs = length(indecies_sq); 

%% data loading
% load MAT files with data
load(test_labels_full_fname);
load(test_images_full_fname);
num_test_images = size(test_images,1);
if verbose
    disp(['Loaded ', num2str(num_test_images) ,' test images']);
end
num_labels = length(shape_labels);

% load relevance matricies
for s = 1:num_labels
    selected_class = shape_labels(s);
    switch selected_class
        case 0
            select_label = 'square';
        case 2
            select_label = 'triangle';
    end
    relevance_fullfname = fullfile(path2experiments,...
        [relevance_fname_base '_selected_' select_label '.mat']);
    load(relevance_fullfname);
    switch selected_class
        case 0
            rel_matrix_sq = rel_matrix;
        case 2
            rel_matrix_tri = rel_matrix;
    end
end

%% take the selected images and relevance maps only
for i =  1:num_shape_pairs
%for i =  1
    index_tri = indecies_tri(i);
    index_sq = indecies_sq(i);
    image_tri = permute(reshape(test_images(index_tri,:), im_dim), res_order);
    image_sq = permute(reshape(test_images(index_sq,:), im_dim), res_order);
    image_tri_rgbimg =  render.shape_to_rgb(round(image_tri*255),3);
    image_sq_rgbimg =  render.shape_to_rgb(round(image_sq*255),3);
    image_tri_rgbimg =  permute(image_tri_rgbimg, res_order);
    image_sq_rgbimg =  permute(image_sq_rgbimg, res_order);
    
    if normalize
        map_sq_sq = normalize_relevance_map(rel_matrix_sq(index_sq,:));
        map_sq_tri = normalize_relevance_map(rel_matrix_tri(index_sq,:));
        map_tri_sq = normalize_relevance_map(rel_matrix_sq(index_tri,:));
        map_tri_tri = normalize_relevance_map(rel_matrix_tri(index_tri,:));
    else
        map_sq_sq =  rel_matrix_sq(index_sq,:);
        map_sq_tri = rel_matrix_tri(index_sq,:);
        map_tri_sq =  rel_matrix_sq(index_tri,:);
        map_tri_tri = rel_matrix_tri(index_tri,:);
    end
    rel_map_sq_sq = reshape(map_sq_sq, im_dim);
    rel_map_sq_tri = reshape(map_sq_tri, im_dim);
    
    rel_map_tri_sq = reshape(map_tri_sq, im_dim);
    rel_map_tri_tri = reshape(map_tri_tri, im_dim);
    
    % make rgb for visualization
    rel_map_sq_sq_rgbimg = permute(render.hm_to_rgb(rel_map_sq_sq,image_sq,3,[],1), res_order);
    rel_map_sq_tri_rgbimg = permute(render.hm_to_rgb(rel_map_sq_tri,image_sq,3,[],1), res_order);
    rel_map_tri_sq_rgbimg = permute(render.hm_to_rgb(rel_map_tri_sq,image_tri,3,[],1), res_order);
    rel_map_tri_tri_rgbimg = permute(render.hm_to_rgb(rel_map_tri_tri,image_tri,3,[],1), res_order);
    
    %% visualize
    figure('units','normalized','outerposition',[0 0 1 1]);
    if subplots
        subplot(131);
    end
    imagesc(image_sq_rgbimg); colormap(gca, gray); colorbar; axis square; 
    if subplots
        axis on, grid on;
    end
    if titles
        title(['Shape ' num2str(index_sq) ': square']);
    end
    if subplots
        subplot(132);
    else
        figure('units','normalized','outerposition',[0 0 1 1]);
    end
    imagesc(rel_map_sq_sq_rgbimg); colormap(gca, jet); colorbar;axis square; 
    if subplots
        axis on, grid on;
    end
    if titles
        title('Relevance: class square');
    end
    
    if subplots
        subplot(133);
    else
        figure('units','normalized','outerposition',[0 0 1 1]);
    end
    imagesc(rel_map_sq_tri_rgbimg); colormap(gca, jet); colorbar; axis square; 
    if subplots
        axis on, grid on;
    end
    if titles
        title('Relevance: class triangle');
    end
    
    
    figure('units','normalized','outerposition',[0 0 1 1])
    if subplots
        subplot(131);
    end
    imagesc(image_tri_rgbimg); colormap(gca, gray); colorbar; axis square; 
    if subplots
        axis on, grid on;
    end
    if titles
        title(['Shape ' num2str(index_tri) ': triangle']);
    end
    if subplots
        subplot(132);
    else
        figure('units','normalized','outerposition',[0 0 1 1]);
    end
    imagesc(rel_map_tri_sq_rgbimg); colormap(gca, jet); axis square;colorbar; 
    if subplots
        axis on, grid on;
    end
    % if titles
    %     if normalize
    %         title('Normalized relevance: class "square"');
    %     else
    %         title('Original relevance: class "square"');
    %     end
    % end
    if titles
        title('Relevance: class square');
    end
    
    if subplots
        subplot(133);
    else
        figure('units','normalized','outerposition',[0 0 1 1]);
    end
    imagesc(rel_map_tri_tri_rgbimg); colormap(gca, jet); axis square; colorbar;axis on, grid on;
    % if titles
    %      if normalize
    %         title('Normalized relevance: class "triangle"');
    %     else
    %         title('Original relevance: class "triangle"');
    %     end
    % end
    if titles
        title('Relevance: class triangle');
    end
end