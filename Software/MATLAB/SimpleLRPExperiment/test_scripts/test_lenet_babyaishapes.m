% test_lenet_babyaishapes.m - testing the performance of the LeNet5 CNN on the BabaAIShapes dataset

% this script uses LRP Toolbox v.1.2.0

%% parameters
config;

verbose = true;

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
lenet5 = model_io.read(full_model_fname);
if verbose
    disp('Loading the pre-trained model...');
end

%% pass the test data through the trained model
Pred = lenet5.forward(test_images);
[~,argmaxPred]  = max(Pred,[],2);
[~,argmaxTruth] = max(test_labels,[],2);
acc = mean(argmaxPred == argmaxTruth);
disp(['Accuracy on the test set: ' num2str(acc*100)]);