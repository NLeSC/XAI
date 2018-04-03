% config.m - setting configurable parameters

project_path = 'C:/Projects/eStep/XAI';
path2originalBabyAIShapes = fullfile(project_path,'/Data/BabyAIShape/shapeset');
train_amat_fname = 'shapeset1_1c_2s_3po.10000.train.amat';
test_amat_fname = 'shapeset1_1c_2s_3po.5000.test.amat';
valid_amat_fname = 'shapeset1_1c_2s_3po.5000.valid.amat';
train_full_fname = fullfile(path2originalBabyAIShapes, train_amat_fname);
test_full_fname = fullfile(path2originalBabyAIShapes, test_amat_fname);
valid_full_fname = fullfile(path2originalBabyAIShapes, valid_amat_fname);

path2matBabyAIShapes = fullfile(project_path,'/Data/BabyAIShape/shapeset_mat');
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