% demo_lrp_exp_lenet_babyaishapes.m - demo experiment for LRP heatmaps on LeNet5 CNN on the BabaAIShapes dataset

% this script uses LRP Toolbox v.1.2.0

%% parameters
config_params;

verbose = false;

num_examples = 15;

%arch = input('Chose architecture (1 = lenet5_sumpool, 2 = lenet3_maxpool): ');
arch = 2;

%% load MAT files with data
load(test_images_full_fname);
num_test_images = size(test_images,1);
load(test_labels_full_fname);
if verbose
    disp(['Loaded ', num2str(num_test_images) ,' test images and labels']);
end

%% select random samples for demonstration
ind_squares = find(test_labels == 0);
ind_squares = ind_squares(randperm(length(ind_squares)));
ind_squares5 = ind_squares(1:5);
ind_circles = find(test_labels == 1);
ind_circles = ind_circles(randperm(length(ind_circles)));
ind_circles5 = ind_circles(1:5);
ind_triangles = find(test_labels == 2);
ind_triangles = ind_triangles(randperm(length(ind_triangles)));
ind_triangles5 = ind_triangles(1:5);

%% normalize & reshape the data and labels
original_test_images = test_images;
[test_images] = normalize_input4lenet(test_images, im_dim, num_channels, reshape_order);
if verbose
    disp(['Normaised ', num2str(num_test_images) ,' test images']);
end
[test_labels] = reshape_labels(test_labels);
if verbose
    disp(['Reshaped ', num2str(num_test_images) ,' test labels']);
end

%% load the model
switch arch
    case 1
        lenet = model_io.read(lenet5_sumpool_full_model_fname);
    case 2
        lenet = model_io.read(lenet3_maxpool_full_model_fname);
end
if verbose
    disp('Loading the pre-trained model...');
end


%% dispay heat maps per each of the selected classes and methods
for selected_class = 1:3
    s = selected_class - 1;
    switch s
        case 0
            select_label = 'square';
        case 1
            select_label = 'circle';
        case 2
            select_label = 'triangle';
    end
    if verbose
        fprintf('Selected Class:      %d: %s\n', s, select_label);
    end
    select = (1:size(test_labels,2) == selected_class)*1.;
    for method = 1:3
    %for method = 2
        figure('units','normalized','outerposition',[0 0 1 1]);
        sbplt = 0;
        for class = 1:3
            
            for counter = 1:5
                switch class
                    case 1
                        index = ind_squares5(counter);
                    case 2
                        index = ind_circles5(counter);
                    case 3
                        index = ind_triangles5(counter);
                end
                sbplt = sbplt + 1;
                test_image = test_images(index,:,:,:);
                original_test_image = reshape(original_test_images(index,:),[32 32]);
                pred_label = lenet.forward(test_image);
                
                [~,pred] = max(pred_label);
                
                switch pred-1
                    case 0
                        pred_class = 'square';
                    case 1
                        pred_class = 'circle';
                    case 2
                        pred_class = 'triangle';
                end
                if verbose
                    fprintf('Predicted Class: %d: %s \n\n', pred-1, pred_class);
                end
                
                %compute first layer relevance according to prediction
                switch method
                    case 1
                        R = lenet.lrp(select);   %as Eq(56) from DOI: 10.1371/journal.pone.0130140
                        tit_str = 'LRP: ratio local and global pre-activtatons';
                    case 2
                        R = lenet.lrp(select,'epsilon',1.);   %as Eq(58) from DOI: 10.1371/journal.pone.0130140
                        tit_str = 'LRP: Using stabilizer  epsilon: 1';
                    case 3
                        R = lenet.lrp(select,'alphabeta',2);    %as Eq(60) from DOI: 10.1371/journal.pone.0130140
                        tit_str = 'LRP: Using alpha-beta rule: 2';
                end
                switch arch
                    case 1
                        title_str = [tit_str ', model: lenet5\_sumpool'];
                    case 2
                        title_str = [tit_str ', model: lenet3\_maxpool'];
                end
                
                %render input and heatmap as rgb images
                shape = render.shape_to_rgb(round(original_test_image*255),3);
                shape = permute(shape,[2 1 3]);
                hm = render.hm_to_rgb(R,test_image,3,[],2);
                img = render.save_image({shape,hm},'../heatmap.png');
                subplot(3,5,sbplt);
                imshow(img); axis off ; drawnow;
                title(['Pred.: ' pred_class ' | Selected: ' select_label ]);
            end
        end
        
        ha = axes('Position',[0 0 1 1],'Xlim',[0 1],'Ylim',[0  1],'Box','off','Visible','off','Units','normalized', 'clipping' , 'off');
        t = text(0.5, 0.98,title_str); t.FontSize = 14; t.FontWeight = 'bold';
    end
    delete('../heatmap.png');
end

