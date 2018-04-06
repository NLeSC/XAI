% test_amat_loader - testing script for the amat format loader

%% parameters
config_params;

verbose = true;
visualize = true;
sav = false;

%% loading of the files
[train_images, train_labels, train_colors] = amat_loader(train_full_fname);
num_train_images = size(train_images,1);
if verbose
    disp(['Loaded ', num2str(num_train_images) ,' train images']);
end
[test_images, test_labels, test_colors] = amat_loader(test_full_fname);
num_test_images = size(test_images,1);
if verbose
    disp(['Loaded ', num2str(num_test_images) ,' test images']);
end
[valid_images, valid_labels, valid_colors] = amat_loader(valid_full_fname);
num_val_images = size(valid_images,1);
if verbose
    disp(['Loaded ', num2str(num_val_images) ,' validation images']);
end


%% visualizaiton
if visualize
    % select 6 random images from the train set
   % train_indicies = randi(num_train_images, 1, 6);
    figure(1);
    for i = 1:6
        subplot(2,3,i);
 %       shape = reshape(train_images(train_indicies(i),:),32,32);
        shape = reshape(train_images(i,:),32,32);
        imshow(shape);
        if i==1
            title('Train set random subset');
        end        
        hold on;
    end
    hold off;
    
    % select 6 random images from the test set
    test_indicies = randi(num_test_images, 1, 6);
    figure(2);
    for i = 1:6      
        subplot(2,3,i);
      %  shape = reshape(test_images(test_indicies(i),:),32,32);
        shape = reshape(test_images(i,:),32,32);
        imshow(shape);
        if i==1
            title('Test set random subset');
        end
        hold on;
    end
    hold off;
    
    % select 6 random images from the valid set
    valid_indicies = randi(num_val_images, 1, 6);
    figure(3);
    for i = 1:6
        subplot(2,3,i);
       % shape = reshape(valid_images(valid_indicies(i),:),32,32);
        shape = reshape(valid_images(i,:),32,32);
        imshow(shape);
        if i==1
            title('Validation set random subset');
        end        
        hold on;
    end
    hold off;
end

%% saving the matricies into MAT files
if sav
    save(train_images_full_fname, 'train_images');
    save(train_labels_full_fname, 'train_labels');
    if verbose
        disp(['Saved ', num2str(num_train_images) ,' train images and their labels in MAT files']);
    end
    save(test_images_full_fname, 'test_images');
    save(test_labels_full_fname, 'test_labels');
    if verbose
        disp(['Saved ', num2str(num_test_images) ,' test images and their labels in MAT files']);
    end
    save(valid_images_full_fname, 'valid_images');
    save(valid_labels_full_fname, 'valid_labels');    
    if verbose
        disp(['Saved ', num2str(num_val_images) ,' validation images and their labels in MAT files']);
    end
end

