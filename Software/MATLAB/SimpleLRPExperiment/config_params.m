% config_params.m - setting configurable parameters for BabyAIShapes experiments

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


path2models = fullfile(project_path, '/Results/Models');
lenet5_sumpool_model_fname = 'lenet5_sumpool_shapeset1_1c_2s_3po.mat';
lenet5_sumpool_full_model_fname = fullfile(path2models, lenet5_sumpool_model_fname);
lenet3_maxpool_model_fname = 'lenet3_maxpool_shapeset1_1c_2s_3po.mat';
lenet3_maxpool_full_model_fname = fullfile(path2models, lenet3_maxpool_model_fname);
lenet5_maxpool_model_fname = 'lenet5_maxpool_shapeset1_1c_2s_3po.mat';
lenet5_maxpool_full_model_fname = fullfile(path2models, lenet5_maxpool_model_fname);

% image dimentions and reshape order
im_dim = [32 32]; 
num_channels = 1;
reshape_order = [1 3 2 4];

%% define BG and FG points
% see the comments of issue #9: https://github.com/NLeSC/XAI/issues/9
bg_point = [1 1];
fg_point = [15 12];