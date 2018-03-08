% train_lenet5MP_mnist.m - training of the LeNet-5 max pooling architecture on MNIST data
%% parameters
project_path = 'C:/Projects/eStep/XAI';
path2trainImages = fullfile(project_path,'/Data/MNIST/images/train');
path2testImages = fullfile(project_path,'/Data/MNIST/images/test');
%path2datastores = fullfile(project_path,'/Data/MNIST/imageDatastores');
verbose = true;
visualize = true;

%% load the images and create datastores

if verbose
    disp('Creating training and testing datastores');
end
trainingMNISTimds = imageDatastore(path2trainImages,...
    'IncludeSubfolders',true,'FileExtensions','.png','LabelSource','foldernames');
%save(fullfile(path2datastores,'trainMNISTimds.mat'),'trainMNISTimds');

testMNISTimds = imageDatastore(path2testImages,...
    'IncludeSubfolders',true,'FileExtensions','.png','LabelSource','foldernames');
%save(fullfile(path2datastores,'testMNISTimds.mat'),'testMNISTimds');

%% display some of the images
if visualize
    figure; 
    perm = randperm(60000,20);
    for i = 1:20
        subplot(4,5,i);
        imshow(trainingMNISTimds.Files{perm(i)});
    end
if verbose
    disp('Example of 20 random training MNIST images');
end
end

%% number of images per category
% Calculate the number of images in each category. |labelCount| is a table
if verbose
    labelCount = countEachLabel(trainingMNISTimds);
    disp(labelCount);
end

%% split into training and validation sets
if verbose
    disp('Splitting the training datastore to training and validaiton datastroes');
end
trainNumFiles = fix(0.8*min(labelCount.Count));
if verbose
    disp([num2str(trainNumFiles) ' number of images per class are used for training...']);
end
[trainMNISTimds,valMNISTimds] = splitEachLabel(trainingMNISTimds,trainNumFiles,'randomize');

%% define the NN architecture
if verbose
    disp('Defining LeNet-5 max pooling architecture...');
end
[layers] = lenet5MP_mnist_arch();

%% Specify Training Options
options = trainingOptions('sgdm',...
    'MaxEpochs',3, ...
    'ValidationData',valMNISTimds,...
    'ValidationFrequency',30,...
    'Verbose',false,...
    'Plots','training-progress');

%% Train Network Using Training Data
if verbose
    disp('Training on MNIST data...');
end
net = trainNetwork(trainMNISTimds,layers,options);


