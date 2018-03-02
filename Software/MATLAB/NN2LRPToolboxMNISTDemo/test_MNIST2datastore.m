% test_MNIST2datastore.m - tesing script

%% parameters
project_path = 'C:/Projects/eStep/XAI';
path2MNIST = fullfile(project_path,'/Data/MNIST/original');
train_images_fname = 'train-images.idx3-ubyte';
test_images_fname = 't10k-images.idx3-ubyte';
train_labels_fname = 'train-labels.idx1-ubyte';
test_labels_fname = 't10k-labels.idx1-ubyte';
path2trainImages = fullfile(project_path,'/Data/MNIST/images/train');
path2testImages = fullfile(project_path,'/Data/MNIST/images/test');
path2datastores = fullfile(project_path,'/Data/MNIST/imageDatastores');
verbose = true;
visualize = false;

%% load original files to matricies and vectors
if verbose
    disp('Loading original MNIST files ot matricies and vectors...');
end
[train_images,train_labels] = loadMNIST2MAT(fullfile(path2MNIST, train_images_fname),...
    fullfile(path2MNIST, train_labels_fname));

[test_images,test_labels] = loadMNIST2MAT(fullfile(path2MNIST, test_images_fname),...
    fullfile(path2MNIST, test_labels_fname));


%% visualize
if visualize
    
    % visualize some test images
    if verbose
        disp('Visualizing some train images ...');
    end
    figure                                          % initialize figure
    colormap(gray)                                  % set to grayscale
    for i = 1:36                                    % preview first 36 samples
        subplot(6,6,i)                              % plot them in 6 x 6 grid
        digit = reshape(train_images(i,:), [28,28]);     % row = 28 x 28 image
        imagesc(digit)                              % show the image
        title(num2str(train_labels(i)))                   % show the label
    end
    
    % visualize some test images
    if verbose
        disp('Visualizing some test images ...');
    end
    figure                                          % initialize figure
    colormap(gray)                                  % set to grayscale
    for i = 1:36                                    % preview first 36 samples
        subplot(6,6,i)                              % plot them in 6 x 6 grid
        digit = reshape(test_images(i,:), [28,28]);     % row = 28 x 28 image
        imagesc(digit)                              % show the image
        title(num2str(test_labels(i)))                   % show the label
    end
    
end

%% save matricies to images with folders indication labels
if verbose
    disp('Saving testing images to folder...');
end
MAT2imageFiles(test_images, test_labels, path2testImages);

if verbose
    disp('Saving training images to folder...');
end
MAT2imageFiles(train_images, train_labels, path2trainImages);

%% create image datastores
trainMNISTimds = imageDatastore(path2trainImages,...
'IncludeSubfolders',true,'FileExtensions','.png','LabelSource','foldernames');
save(fullfile(path2datastores,'trainMNISTimds.mat'),'trainMNISTimds');

testMNISTimds = imageDatastore(path2testImages,...
'IncludeSubfolders',true,'FileExtensions','.png','LabelSource','foldernames');
save(fullfile(path2datastores,'testMNISTimds.mat'),'testMNISTimds');