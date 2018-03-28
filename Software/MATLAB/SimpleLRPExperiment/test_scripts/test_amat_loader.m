% test_amat_loader - testing script for the amat format loader

%% parameters
project_path = 'C:/Projects/eStep/XAI';
path2BabyAIShapes = fullfile(project_path,'/Data/BabyAIShape/shapeset');
train_amat_fname = 'shapeset1_1c_2s_3po.10000.train.amat';
test_amat_fname = 'shapeset1_1c_2s_3po.5000.test.amat';
valid_amat_fname = 'shapeset1_1c_2s_3po.5000.valid.amat';
train_full_fname = fullfile(path2BabyAIShapes, train_amat_fname);
test_full_fname = fullfile(path2BabyAIShapes, test_amat_fname);
valid_full_fname = fullfile(path2BabyAIShapes, valid_amat_fname);

verbose = true;
visualize = true;

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
    train_indicies = randi(num_train_images, 1, 6);
    figure(1);
    for i = 1:6
        
        subplot(2,3,i);
        shape = reshape(train_images(train_indicies(i),:),32,32);
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
        shape = reshape(test_images(test_indicies(i),:),32,32);
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
        shape = reshape(valid_images(valid_indicies(i),:),32,32);
        imshow(shape);
        if i==1
            title('Validation set random subset');
        end        
        hold on;
    end
    hold off;
end


