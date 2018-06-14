% train_nn_tri_sq_rot.m - testing the training of a neural network (nn)
% for the triangles and squares rotation dataset

% Comment: It is a copy of train_lenet_tri_sq_rot.m meant for general 
% neural network architectures.

% this script uses LRP Toolbox v.1.2.0

%% parameters
config_params_tri_sq;

verbose = true;
save = true;

%arch = input('Chose architecture (1 = lenet5_maxpool): ');
%arch = 1;  % lenet5_maxpool
arch = 2;  % short relu

%% load MAT files with data
load(train_images_full_fname);
num_train_images = size(train_images,1);
load(train_labels_full_fname);
if verbose
     disp(['Loaded ', num2str(num_train_images) ,' train images and labels']);
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
     disp(['Normalised ', num2str(num_train_images) ,' train images']);
end
[train_labels] = reshape_labels(train_labels);
if verbose
     disp(['Reshaped ', num2str(num_train_images) ,' train labels']);
end
[valid_images] = normalize_input4lenet(valid_images, im_dim, num_channels, reshape_order);
if verbose
     disp(['Normalised ', num2str(num_valid_images) ,' valid images']);
end
[valid_labels] = reshape_labels(valid_labels);
if verbose
     disp(['Reshaped ', num2str(num_valid_images) ,' valid labels']);
end

if arch == 2
   % reshape data
   train_images = reshape(train_images, [size(train_images,1), im_dim(1)^2]);
   valid_images = reshape(valid_images, [size(valid_images,1), im_dim(1)^2]);
end

%% create LeNet CNN
switch arch
    case 1
        [net] = lenet5_maxpool_arch2();
    case 2
        [net] = short_relu_arch();
    otherwise
        error("Unknown architecture!");
end

%% train the network
%train the net
if verbose
     disp('Training LeNet on the training images using the validation images');
end
net.train(train_images,train_labels,valid_images,valid_labels,25,num_train_iter,0.0001);

%% save the model
if save
    switch arch
        case 1
            full_model_fname = lenet5_maxpool_full_model_fname;
        case 2
            full_model_fname = short_relu_full_model_fname;
        otherwise
            error("Unknown architecture!");
    end
    model_io.write(net, full_model_fname);
    if verbose
        disp('Saving the model...');
    end
end
