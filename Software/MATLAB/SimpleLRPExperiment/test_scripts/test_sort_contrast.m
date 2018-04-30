% test_sort_contrast - sorting test images by contrast

%% parameters
config_params;

verbose = true;
visualize = true;
sav = false;

start_index = 1000;
step = 10;

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
    % select 15 consequtive images from the test set
    figure('units','normalized','outerposition',[0 0 1 1]);
    count = 0;
    for i = 1:step:15*step
        count = count + 1;
        subplot(3,5,count);
        shape = reshape(sorted_squares(start_index + i,:),32,32);
        imshow(shape);
        hold on;
    end
    hold off;
    title_str = ['Test set: 15 sorted square images starting at image ' num2str(start_index) ' with step of ' num2str(step)];
    axes('Position',[0 0 1 1],'Xlim',[0 1],'Ylim',[0  1],'Box','off','Visible','off','Units','normalized', 'clipping' , 'off');
    t = text(0.5, 0.98,title_str); t.FontSize = 14; t.FontWeight = 'bold';
    
    figure('units','normalized','outerposition',[0 0 1 1]);
    count = 0;
    for i = 1:step:15*step
        count = count + 1;
        subplot(3,5,count);
        shape = reshape(sorted_circles(start_index + i,:),32,32);
        imshow(shape);
        hold on;
    end
    hold off;
    title_str = ['Test set: 15 sorted circle images starting at image ' num2str(start_index) ' with step of ' num2str(step)];
    axes('Position',[0 0 1 1],'Xlim',[0 1],'Ylim',[0  1],'Box','off','Visible','off','Units','normalized', 'clipping' , 'off');
    t = text(0.5, 0.98,title_str); t.FontSize = 14; t.FontWeight = 'bold';
    
    figure('units','normalized','outerposition',[0 0 1 1]);
    count = 0;
    for i = 1:step:15*step
        count = count + 1;
        subplot(3,5,count);
        shape = reshape(sorted_triangles(start_index + i,:),32,32);
        imshow(shape);
        hold on;
    end
    hold off;
    title_str = ['Test set: 15 sorted triangle images starting at image ' num2str(start_index) ' with step of ' num2str(step)];
    axes('Position',[0 0 1 1],'Xlim',[0 1],'Ylim',[0  1],'Box','off','Visible','off','Units','normalized', 'clipping' , 'off');
    t = text(0.5, 0.98,title_str); t.FontSize = 14; t.FontWeight = 'bold';
    
end
