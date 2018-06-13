% config_params_tri_sq_rot.m - setting configurable parameters for Tringles and Squares rotation experiments

%binary = input('Process Binary dataset? Binary=true, Gray=false. [1=true|0=false]: ');
binary = false;
%save_relevance = input('Save relevance matrix and predicted classes? [1=true|0=false]: ');
save_relevance = true;
%save_evidence = input('Save evidence statistics? [1=true|0=false]: ');
save_evidence = true;

%arch = input('Chose architecture (1 = lenet5_maxpool, 2= short_relu): ');
%arch = 1;  % lenet5_maxpool
arch = 2;  % short relu 

num_train_iter = 20000;

shape_labels = [0,2]; % [square triangle]

[~, name] = system('hostname');  % finds the name of the system
if strcmp(name, ['XPS13-2vgkmh2' newline])
    % project path on Joost his CWI laptop
    project_path = 'C:\Users\berkhout\Desktop\XAI';
else
    project_path = 'C:/Projects/eStep/XAI';
end

if binary
    path2matTrianglesAndSquaresShapes = fullfile(project_path,'/Data/TrianglesAndSquaresRotation/Binary');
else
   % path2matTrianglesAndSquaresShapes = fullfile(project_path,'/Data/TrianglesAndSquaresRotation/Gray');
   path2matTrianglesAndSquaresShapes = fullfile(project_path,'/Data/TrianglesAndSquaresScaleRotation/Gray');
end
train_images_mat_fname = 'TrianglesAndSquares_images_train_50k.mat';
test_images_mat_fname = 'TrianglesAndSquares_images_test_30k.mat';
valid_images_mat_fname = 'TrianglesAndSquares_images_valid_20k.mat';

train_labels_mat_fname = 'TrianglesAndSquares_labels_train_50k.mat';
test_labels_mat_fname = 'TrianglesAndSquares_labels_test_30k.mat';
valid_labels_mat_fname = 'TrianglesAndSquares_labels_valid_20k.mat';

test_bands_mat_fname = 'TrianglesAndSquares_bands_test_30k.mat';

train_images_full_fname = fullfile(path2matTrianglesAndSquaresShapes, train_images_mat_fname);
test_images_full_fname = fullfile(path2matTrianglesAndSquaresShapes, test_images_mat_fname);
valid_images_full_fname = fullfile(path2matTrianglesAndSquaresShapes, valid_images_mat_fname);

train_labels_full_fname = fullfile(path2matTrianglesAndSquaresShapes, train_labels_mat_fname);
test_labels_full_fname = fullfile(path2matTrianglesAndSquaresShapes, test_labels_mat_fname);
valid_labels_full_fname = fullfile(path2matTrianglesAndSquaresShapes, valid_labels_mat_fname);

test_bands_full_fname = fullfile(path2matTrianglesAndSquaresShapes, test_bands_mat_fname);


path2models = fullfile(project_path, '/Results/Models');

lenet_model_basename = 'lenet5_maxpool';
if binary
    lenet5_maxpool_model_fname = [lenet_model_basename '_binary_triangles_and_squares_rotation.mat'];
else
    lenet5_maxpool_model_fname = [lenet_model_basename '_gray_triangles_and_squares_rotation.mat'];
end
lenet5_maxpool_full_model_fname = fullfile(path2models, lenet5_maxpool_model_fname);


linear_model_basename = 'two_layer_short_relu';
if binary
    short_relu_model_fname = [linear_model_basename '_binary_triangles_and_squares_rotation.mat'];
else
    %short_relu_model_fname = [linear_model_basename '_gray_triangles_and_squares_rotation.mat'];
    short_relu_model_fname = [linear_model_basename '_gray_triangles_and_squares_scale_rotation.mat'];
end
short_relu_full_model_fname = fullfile(path2models, short_relu_model_fname);

%% relevance
if save_relevance
    path2vid = fullfile(project_path, '/Results/Experiments/TrianglesAndSquares');
    relevance_fname_base = 'TrianglesAndSquares_test_30k_relevance';
    if binary
        path2experiments = fullfile(path2vid, 'Binary');
    else
        path2experiments = fullfile(path2vid, 'Gray');
    end
    switch arch
        case 1
           path2experiments = fullfile(path2experiments, 'lenet5-maxpool');  
        case 2
           path2experiments = fullfile(path2experiments, 'short-relu');  
    end
    predictions_fname_base = 'TrianglesAndSquares_test_30k_predictions.mat';
    predictions_fullfname = fullfile(path2experiments,predictions_fname_base);
    
end

%% evidence
if save_evidence
    evidence_fname_base = 'TrianglesAndSquares_test_30k_evidence.mat';
    if binary
        path2evidence = fullfile(path2vid, 'Binary');
    else
        path2evidence = fullfile(path2vid, 'Gray');
    end
    switch arch
        case 1
           path2evidence = fullfile(path2evidence, 'lenet5-maxpool');  
        case 2
           path2evidence = fullfile(path2evidence, 'short-relu');  
    end
    evidence_fullfname = fullfile(path2evidence,evidence_fname_base);   
end

% image dimentions and reshape order
%im_dim = [32 32];
im_dim = [64 64];
num_channels = 1;
reshape_order = [1 3 2 4];
res_order = [2 1 3];
%% define BG and FG points
% see the comments of issue #9: https://github.com/NLeSC/XAI/issues/9
bg_point = [1 1];
fg_point = [15 12];
