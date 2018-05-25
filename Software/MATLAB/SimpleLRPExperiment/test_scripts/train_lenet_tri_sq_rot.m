% train_lenet_tri_sq_rot.m - testing the training of LeNet5 CNNon the Triangles and Squares rotaiton dataset

% this script uses LRP Toolbox v.1.2.0

%% parameters
config_params_tri_sq_rot;

verbose = true;
sav = true;

%arch = input('Chose architecture (1 = lenet5_maxpool): ');
arch = 1;
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

%% create LeNet CNN
switch arch
    case 1
        [lenet] = lenet5_maxpool_arch2();        
    otherwise
        error("Unknown architecture!");
end

%% train the network
%train the net
if verbose
     disp('Training LeNet on the training images using the validation images');
end
lenet.train(train_images,train_labels,valid_images,valid_labels,25,num_train_iter,0.0001);

%% save the model
if sav
    switch arch
        case 1
            full_model_fname = lenet5_maxpool_full_model_fname;            
        otherwise
            error("Unknown architecture!");
    end
    model_io.write(lenet, full_model_fname);
    if verbose
        disp('Saving the model...');
    end
end
