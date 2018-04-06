% test_sort_contrast - sorting test images by contrast

%% parameters
config_params;

verbose = true;
visualize = true;
sav = false;

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
[sorted_test_images] = sort_contrast(test_images, bg_point, fg_point);
if verbose
    disp(['Sorted ', num2str(num_test_images) ,' test images by contrast']);
end

