% config_params_tri_sq_rot.m - setting configurable parameters for Tringles and Squares rotation experiments


save_relevance = true;
%save_relevance = false;

binary = true;
%binary = false;
num_train_iter = 20000;

shape_labels = [0,2];
project_path = 'C:/Projects/eStep/XAI';

if binary
    path2matTrianglesAndSquaresShapes = fullfile(project_path,'/Data/TrianglesAndSquaresRotation/Binary');
else
    path2matTrianglesAndSquaresShapes = fullfile(project_path,'/Data/TrianglesAndSquaresRotation/Gray');
end
train_images_mat_fname = 'TrianglesAndSquares_images_train_50k.mat';
test_images_mat_fname = 'TrianglesAndSquares_images_test_30k.mat';
valid_images_mat_fname = 'TrianglesAndSquares_images_valid_20k.mat';
train_labels_mat_fname = 'TrianglesAndSquares_labels_train_50k.mat';
test_labels_mat_fname = 'TrianglesAndSquares_labels_test_30k.mat';
valid_labels_mat_fname = 'TrianglesAndSquares_labels_valid_20k.mat';
train_images_full_fname = fullfile(path2matTrianglesAndSquaresShapes, train_images_mat_fname);
test_images_full_fname = fullfile(path2matTrianglesAndSquaresShapes, test_images_mat_fname);
valid_images_full_fname = fullfile(path2matTrianglesAndSquaresShapes, valid_images_mat_fname);
train_labels_full_fname = fullfile(path2matTrianglesAndSquaresShapes, train_labels_mat_fname);
test_labels_full_fname = fullfile(path2matTrianglesAndSquaresShapes, test_labels_mat_fname);
valid_labels_full_fname = fullfile(path2matTrianglesAndSquaresShapes, valid_labels_mat_fname);


path2models = fullfile(project_path, '/Results/Models');

if binary
    lenet5_maxpool_model_fname = 'lenet5_maxpool_binary_triangles_and_squares_rotation.mat';
else
    lenet5_maxpool_model_fname = 'lenet5_maxpool_gray_triangles_and_squares_rotation.mat';
end
lenet5_maxpool_full_model_fname = fullfile(path2models, lenet5_maxpool_model_fname);

path2exper = fullfile(project_path, '/Results/Experiments/TrianglesAndSquares');
relevance_fname_base = 'TrianglesAndSquares_test_30k_relevance';
if binary
    path2experiments = fullfile(path2exper, 'Binary');
else
    path2experiments = fullfile(path2exper, 'Gray');
end


% image dimentions and reshape order
im_dim = [32 32]; 
num_channels = 1;
reshape_order = [1 3 2 4];
%% define BG and FG points
% see the comments of issue #9: https://github.com/NLeSC/XAI/issues/9
bg_point = [1 1];
fg_point = [15 12];