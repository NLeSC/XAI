% demo_lrp_exp_nn_tri_sq_rot.m - demo experiment for LRP heatmaps on 
% general neural networks (nn) on the Triangles and Squares dataset.
% This script file is a copy of demo_lrp_exp_lenet_tri_sq_rot.m but then
% created for general neural networks.

% this script uses LRP Toolbox v.1.2.0

%% parameters
config_params_tri_sq_rot;

unique_flag = true;

verbose = true;
visualize = true;
num_examples = 15;
start_index = 1;
start_indicies = 1;% :15:31; %1500-75;
step = 1;

%arch = input('Chose architecture (1 = lenet5_maxpool): ');
%arch = 1;  % lenet5_maxpool
arch = 2;  % short relu

%% data loading
% load MAT files with data
load(test_images_full_fname);
num_test_images = size(test_images,1);
load(test_labels_full_fname);
if verbose
    disp(['Loaded ', num2str(num_test_images) ,' test images and labels']);
end

% split the images per shape
for shape_label = shape_labels
    shape_index = find(test_labels == shape_label);
    input_1shape_images = test_images(shape_index,:);
    switch shape_label
        % or stands most likely for original
        case 0
            or_squares = input_1shape_images;            
        case 2
            or_triangles = input_1shape_images;
    end
    
end

if verbose
    disp(['Splited ', num2str(num_test_images) ,' test images by shape type']);
end
%if visualize
%    visualize_1shape(or_squares, 0, num_examples, start_index, step);
%    visualize_1shape(or_triangles, 2, num_examples, start_index, step);
%end

%% normalize & reshape the data and labels
[squares] = normalize_input4lenet(or_squares, im_dim, num_channels, reshape_order);
[triangles] = normalize_input4lenet(or_triangles, im_dim, num_channels, reshape_order);
if verbose
    disp(['Normalized ', num2str(num_test_images) ,' test images']);
end
[test_labels] = reshape_labels(test_labels);
if verbose
    disp(['Reshaped ', num2str(num_test_images) ,' test labels']);
end

if arch == 2
   % reshape data
   squares = reshape(squares, [size(squares,1), 32^2]);
   triangles = reshape(triangles, [size(triangles,1), 32^2]);
end

%% load the model
switch arch
    case 1
        lenet = model_io.read(lenet5_maxpool_full_model_fname);
    case 2
        lenet = model_io.read(short_relu_full_model_fname);
end
if verbose
    disp('Loaded the pre-trained model.');
end

%% compute and dispay heat maps per each of the selected classes and methods
for s = 1:length(shape_labels)
    % s is the index of the selected shape for heatmap
    
    selected_class = shape_labels(s);
    switch s
        case 1
            select_label = 'square';            
        case 2
            select_label = 'triangle';
            
    end
%     if verbose
%         fprintf('Selected Class:      %d: %s\n', s, select_label);
%     end
    select = (1:size(test_labels,2) == s)*1.;
    %for method = 1:3
    for method = 3
        for c = 1:length(shape_labels)
            % c is the index of the true shape
            
            class = shape_labels(c);
            switch class
                case 0
                    class_label = 'square';
                case 2
                    class_label = 'triangle';                    
            end
            for start_index = start_indicies
                if visualize
                    figure('units','normalized','outerposition',[0 0 1 1]);
                    subplts = numSubplots(num_examples);
                    sbplt_rows = subplts(1); sbplt_cols = subplts(2);
                    hold on
                end
                counter = 0;
                for i = 1:step:num_examples*step
                    counter = counter + 1;
                    switch c
                        case 1
                            index = i + start_index;
                            test_image = squares(index,:,:,:);
                            or_image = or_squares(index,:,:,:);                        
                        case 2
                            index = i + start_index;
                            test_image = triangles(index,:,:,:);
                            or_image = or_triangles(index,:,:,:);
                    end
                    
                    [comp_hm, R, pred, gray_diff] = compute_lrp_heatmap(or_image, test_image, im_dim, ...
                        lenet, method, select, shape_labels);
                                        
                    if visualize
                        subplot(sbplt_rows, sbplt_cols,counter);
                        imshow(comp_hm); axis off ; drawnow;
                    end
                    
                    switch pred
                        case 0  % I think this should be 0 instead of 1?
                            pred_class = 'square';
                        case 2
                            pred_class = 'triangle';                            
                    end
%                     if verbose
%                         fprintf('Predicted Class: %d: %s \n\n', pred-1, pred_class);
%                     end
                    switch method
                        case 1
                            tit_str = ' LRP: ratio local and global pre-activtatons';
                        case 2
                            tit_str = 'LRP: Using stabilizer  epsilon: 1';
                        case 3
                            tit_str = ' LRP: Using alpha-beta rule: 2';
                    end
                    switch arch
                        case 1
                            titl_str = [tit_str ', model: lenet5\_maxpool'];
                        case 2
                            titl_str = [tit_str ', model: short\_relu'];
                    end
                    
                    if visualize
                        title(['Pred.: ' pred_class ' | Selected: ' select_label ]);
                        xlabel(['Abs. gray val. diff: ', num2str(gray_diff)]);
                    end
                end
                if visualize
                    title_str = ['LRP on test set: 15 ' class_label ...
                        ' images starting at image ' num2str(start_index) ...
                        ' with step of ' num2str(step) '.' titl_str];
                    axes('Position',[0 0 1 1],'Xlim',[0 1],'Ylim',[0  1],'Box','off','Visible','off','Units','normalized', 'clipping' , 'off');
                    t = text(0.3, 0.98,title_str); t.FontSize = 14; t.FontWeight = 'bold';
                end
                
            end
        end
        
    end
    
end

