% test_train_lenet_babyaishapes.m - testing the training of LeNet5 CNNon the BabaAIShapes dataset

% this script uses LRP Toolbox v.1.2.0

%% parameters
project_path = 'C:/Projects/eStep/XAI';
path2matBabyAIShapes = fullfile(project_path,'/Data/BabyAIShape/shapeset_mat');
path2model = fullfile(project_path, '/Results/Models');
model_fname = 'lenet5_shapeset1_1c_2s_3po.mat';
full_model_fname = fullfile(path2model, model_fname);
train_images_mat_fname = 'shapeset1_1c_2s_3po.10000.train_images.mat';
test_images_mat_fname = 'shapeset1_1c_2s_3po.5000.test_images.mat';
valid_images_mat_fname = 'shapeset1_1c_2s_3po.5000.valid_images.mat';
train_labels_mat_fname = 'shapeset1_1c_2s_3po.10000.train_labels.mat';
test_labels_mat_fname = 'shapeset1_1c_2s_3po.5000.test_labels.mat';
valid_labels_mat_fname = 'shapeset1_1c_2s_3po.5000.valid_labels.mat';
train_images_full_fname = fullfile(path2matBabyAIShapes, train_images_mat_fname);
test_images_full_fname = fullfile(path2matBabyAIShapes, test_images_mat_fname);
valid_images_full_fname = fullfile(path2matBabyAIShapes, valid_images_mat_fname);
train_labels_full_fname = fullfile(path2matBabyAIShapes, train_labels_mat_fname);
test_labels_full_fname = fullfile(path2matBabyAIShapes, test_labels_mat_fname);
valid_labels_full_fname = fullfile(path2matBabyAIShapes, valid_labels_mat_fname);


im_dim = [32 32]; 
num_channels = 1;
reshape_order = [1 3 2 4];

verbose = true;
sav = true;

%% load MAT files with data
load(train_images_full_fname);
num_train_images = size(train_images,1);
load(train_labels_full_fname);
if verbose
     disp(['Loaded ', num2str(num_train_images) ,' train images and labels']);
end
load(test_images_full_fname);
num_test_images = size(test_images,1);
load(test_labels_full_fname);
if verbose
     disp(['Loaded ', num2str(num_test_images) ,' test images and labels']);
end
load(valid_images_full_fname);
num_valid_images = size(valid_images,1);
load(valid_labels_full_fname);
if verbose
     disp(['Loaded ', num2str(num_valid_images) ,' valid images and labels']);
end

%% normalize & reshape the data and labels
[train_images] = normalize_input4lenet(train_images, im_dim, num_channels, reshape_order);
if verbose
     disp(['Normaised ', num2str(num_train_images) ,' train images']);
end
[train_labels] = reshape_labels(train_labels);
if verbose
     disp(['Reshaped ', num2str(num_train_images) ,' train labels']);
end
[test_images] = normalize_input4lenet(test_images, im_dim, num_channels, reshape_order);
if verbose
     disp(['Normaised ', num2str(num_test_images) ,' test images']);
end
[test_labels] = reshape_labels(test_labels);
if verbose
     disp(['Reshaped ', num2str(num_test_images) ,' test labels']);
end
[valid_images] = normalize_input4lenet(valid_images, im_dim, num_channels, reshape_order);
if verbose
     disp(['Normalised ', num2str(num_valid_images) ,' valid images']);
end
[valid_labels] = reshape_labels(valid_labels);
if verbose
     disp(['Reshaped ', num2str(num_valid_images) ,' valid labels']);
end

%% create LeNet-5 CNN
[lenet] = lenet_arch();

%% train the network
%train the net
if verbose
     disp('Training LeNet5 on the training images using the validation images');
end
lenet.train(train_images,train_labels,valid_images,valid_labels,25,50000,0.0001);

%% save the model
if sav
    model_io.write(lenet, full_model_fname);
    if verbose
        disp('Saving the model...');
    end
end
