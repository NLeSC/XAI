% test_sort_contrast - sorting test images by contrast

%% parameters
config_params;

verbose = true;
visualize = true;
sav = false;

start_index = 2500;

%% load the MAT test shapes
load(test_images_full_fname); % loaded test_images
num_test_images = size(test_images,1);
if verbose
    disp(['Loaded ', num2str(num_test_images) ,' test images']);
end

%% define BG and FG points
% see the comments of issue #9: https://github.com/NLeSC/XAI/issues/9

bg_point = [1 1];
fg_point = [15 12];

%% sort the images on BG and then on FG gray values
[sorted_test_images, sorted_index] = sort_contrast(test_images, bg_point, fg_point);
if verbose
    disp(['Sorted ', num2str(num_test_images) ,' test images by contrast']);
end

%% visualizaiton
if visualize
    % select 15 consequtive images from the test set
    figure(1);
    count = 0;
    for i = 1:100:1500
        count = count + 1;
        subplot(3,5,count);
        shape = reshape(sorted_test_images(start_index + i,:),32,32);
        imshow(shape);
        hold on;
    end
    hold off;
    title_str = 'Test set 15 sorted images (step 100 images)';
    ha = axes('Position',[0 0 1 1],'Xlim',[0 1],'Ylim',[0  1],'Box','off','Visible','off','Units','normalized', 'clipping' , 'off');
    t = text(0.5, 0.98,title_str); t.FontSize = 14; t.FontWeight = 'bold';
    
end
