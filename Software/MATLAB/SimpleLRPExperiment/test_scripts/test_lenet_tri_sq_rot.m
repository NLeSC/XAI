% test_lenet_tri_sq_rot.m - testing the performance of the LeNet5 CNN on the Triangles & squares dataset

% this script uses LRP Toolbox v.1.2.0

%% parameters
config_params_tri_sq_rot;

verbose = true;

arch = input('Chose architecture (1 = lenet5_maxpool): ');
%% load MAT files with data
load(test_images_full_fname);
num_test_images = size(test_images,1);
load(test_labels_full_fname);
if verbose
     disp(['Loaded ', num2str(num_test_images) ,' test images and labels']);
end

%% normalize & reshape the data and labels
[test_images] = normalize_input4lenet(test_images, im_dim, num_channels, reshape_order);
if verbose
     disp(['Normaised ', num2str(num_test_images) ,' test images']);
end
[test_labels] = reshape_labels(test_labels);
if verbose
     disp(['Reshaped ', num2str(num_test_images) ,' test labels']);
end

%% load the model
switch arch
    case 1
        lenet = model_io.read(lenet5_maxpool_full_model_fname);
    otherwise
        error("Unknown architecture!");
end
if verbose
    disp('Loading the pre-trained model...');
end

%% pass the test data through the trained model
Pred = lenet.forward(test_images);
[~,argmaxPred]  = max(Pred,[],2);
[~,argmaxTruth] = max(test_labels,[],2);
acc = mean(argmaxPred == argmaxTruth);
disp(['Accuracy on the test set: ' num2str(acc*100)]);