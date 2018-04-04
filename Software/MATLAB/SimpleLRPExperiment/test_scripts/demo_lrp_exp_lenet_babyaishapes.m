% demo_lrp_exp_lenet_babyaishapes.m - demon experiemnt forLRP heatmaps on LeNet5 CNN on the BabaAIShapes dataset

% this script uses LRP Toolbox v.1.2.0

%% parameters
config;

verbose = true;

num_examples = 12;

%% load MAT files with data
load(test_images_full_fname);
num_test_images = size(test_images,1);
load(test_labels_full_fname);
if verbose
    disp(['Loaded ', num2str(num_test_images) ,' test images and labels']);
end

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
lenet5 = model_io.read(lenet5_sumpool_full_model_fname);
if verbose
    disp('Loading the pre-trained model...');
end

%% select random samples for demonstration
all_indicies = randperm(num_test_images);
indicies = all_indicies(1:num_examples);

for selected_class = 1:3
    s = selected_class - 1;
    switch s
        case 0
            select_label = 'rectangle';
        case 1
            select_label = 'circle';
        case 2
            select_label = 'triangle';
    end
    fprintf('Selected Class:      %d: %s\n', s, select_label);
    select = (1:size(test_labels,2) == selected_class)*1.;
    %for method = 1:3
    for method = 2
        figure('units','normalized','outerposition',[0 0 1 1]);
        sbplt = 0;
        for i = indicies
            sbplt = sbplt + 1;
            test_image = test_images(i,:,:,:);
            original_test_image = reshape(original_test_images(i,:),[32 32]);
            pred_label = lenet5.forward(test_image);
            
            [~,pred] = max(pred_label);
            
            switch pred-1
                case 0
                    pred_class = 'rectangle';
                case 1
                    pred_class = 'circle';
                case 2
                    pred_class = 'triangle';
            end
            fprintf('Predicted Class: %d: %s \n\n', pred-1, pred_class);
            
            %compute first layer relevance according to prediction
            switch method
                case 1
                    R = lenet5.lrp(select);   %as Eq(56) from DOI: 10.1371/journal.pone.0130140
                    title_str = 'LRP: ratio local and global pre-activtatons';
                case 2
                    R = lenet5.lrp(select,'epsilon',1.);   %as Eq(58) from DOI: 10.1371/journal.pone.0130140
                    title_str = 'LRP: Using stabilizer  epsilon, 1';
                case 3
                    R = lenet5.lrp(select,'alphabeta',2);    %as Eq(60) from DOI: 10.1371/journal.pone.0130140
                    title_str = 'LRP: Using alpha-beta rule, 2';
            end
            
            
            %render input and heatmap as rgb images
            shape = render.shape_to_rgb(round(original_test_image*255),3);
            shape = permute(shape,[2 1 3]);
            hm = render.hm_to_rgb(R,test_image,3,[],2);
            img = render.save_image({shape,hm},'../heatmap.png');
            subplot(3,4,sbplt);
            imshow(img); axis off ; drawnow;
            title(['Selected: ' select_label ' |Pred.: ' pred_class]);
        end
        
        ha = axes('Position',[0 0 1 1],'Xlim',[0 1],'Ylim',[0  1],'Box','off','Visible','off','Units','normalized', 'clipping' , 'off');
        t = text(0.5, 0.98,title_str); t.FontSize = 14; t.FontWeight = 'bold';
    end
    delete('../heatmap.png');
end

