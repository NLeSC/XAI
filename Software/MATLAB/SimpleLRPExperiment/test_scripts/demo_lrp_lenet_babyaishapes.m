% demo_lrp_lenet_babyaishapes.m - demonstrating the LRP heatmaps on LeNet5 CNN on the BabaAIShapes dataset

% this script uses LRP Toolbox v.1.2.0

%% parameters
config;

verbose = true;

num_examples = 15;

arch = input('Chose architecture (1 = lenet5_sumpool, 2 = lenet3_maxpool): ');


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
switch arch
    case 1
        lenet = model_io.read(lenet5_sumpool_full_model_fname);
    case 2
        lenet = model_io.read(lenet3_maxpool_full_model_fname);
end
if verbose
    disp('Loading the pre-trained model...');
end

%% select random samples for demonstration
all_indicies = randperm(num_test_images);
indicies = all_indicies(1:num_examples);

for method = 1:3
    figure('units','normalized','outerposition',[0 0 1 1]);
    sbplt = 0;
    for i = indicies
        sbplt = sbplt + 1;
        test_image = test_images(i,:,:,:);
        original_test_image = reshape(original_test_images(i,:),[32 32]);
        pred_label = lenet.forward(test_image);
        [~,true] = max(test_labels(i,:));
        [~,pred] = max(pred_label);
        
        switch true-1
            case 0
                true_class = 'rectangle';
            case 1
                true_class = 'circle';
            case 2
                true_class = 'triangle';
        end
        fprintf('True Class:      %d: %s\n', true-1, true_class);
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
                R = lenet.lrp(pred_label);   %as Eq(56) from DOI: 10.1371/journal.pone.0130140
                tit_str = 'LRP: ratio local and global pre-activtatons';
            case 2
                R = lenet.lrp(pred_label,'epsilon',1.);   %as Eq(58) from DOI: 10.1371/journal.pone.0130140
                tit_str = 'LRP: Using stabilizer  epsilon: 1';
            case 3
                R = lenet.lrp(pred_label,'alphabeta',2);    %as Eq(60) from DOI: 10.1371/journal.pone.0130140
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
        title(['True: ' true_class ' |Pred.: ' pred_class]);
    end
    
    ha = axes('Position',[0 0 1 1],'Xlim',[0 1],'Ylim',[0  1],'Box','off','Visible','off','Units','normalized', 'clipping' , 'off');
    t = text(0.5, 0.98,title_str); t.FontSize = 14; t.FontWeight = 'bold';
end
delete('../heatmap.png');

