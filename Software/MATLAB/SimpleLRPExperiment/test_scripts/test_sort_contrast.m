% test_sort_contrast - sorting test images by contrast

%% parameters
config_params;

verbose = true;
visualize = true;
sav = false;

start_index = 1000;
step = 10;

num_samples = 15;

%% load the MAT test shapes and their labels
load(test_images_full_fname); % loaded test_images
load(test_labels_full_fname); % loaded test_labels
num_test_images = size(test_images,1);
if verbose
    disp(['Loaded ', num2str(num_test_images) ,' test images']);
end

%% sort the images on BG and then on FG gray values per shape
for shape_label = 0:2
    [sorted_1shape_images, shape_index, sort_1shape_index] = ...
        sort_1shape_contrast(test_images, test_labels, shape_label, bg_point,fg_point);
    switch shape_label
        case 0
            sorted_squares = sorted_1shape_images;
        case 1
            sorted_circles = sorted_1shape_images;
        case 2
            sorted_triangles = sorted_1shape_images;
    end
    
end

if verbose
    disp(['Sorted ', num2str(num_test_images) ,' test images by contrast']);
end

%% visualizaiton
if visualize
    visualize_sorted_shape(sorted_squares, 0, num_samples, start_index, step);
    visualize_sorted_shape(sorted_circles, 1, num_samples, start_index, step);
    visualize_sorted_shape(sorted_triangles, 2, num_samples, start_index, step);
end
