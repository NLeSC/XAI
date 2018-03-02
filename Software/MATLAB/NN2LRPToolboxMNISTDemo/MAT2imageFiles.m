% MAT2imageFiles - saving images from the image MNIST MATLAB matrix 
% **************************************************************************
% function [] = MAT2imageFiles(images, labels, file_path)
%
% author: Elena Ranguelova, NLeSc
% date created: 2 March 2018
% last modification date: 
% modification details: 
%**************************************************************************
% INPUTS:
% images        matrix of images of dimentions Nimages x 784 (28x28)
% labels        column vector of labels of dimentions Nimages x 1
% file_path     path to the root folder saving all 28x28 images in PNG format
%               the subfolder name comes from the corresponding label
%**************************************************************************
% OUTPUTS:
%**************************************************************************
% NOTES: 
% should be used after loadMNIST2MAT function
%**************************************************************************
% EXAMPLES USAGE: 
% 
% see test_script_name.m - cells 1 - 5
%**************************************************************************
% REFERENCES:
%**************************************************************************
function [] = MAT2imageFiles(images, labels, file_path)

% number of images
nimages = length(labels);

% unique labels 
uni_labels = unique(labels);

% create subfolders for each label (digit) category
for l = 1:length(uni_labels)
    label = num2str(uni_labels(l));
    mkdir(fullfile(file_path, label));
end
    

% create images and save them as PNG files
count = 0;
for n = 1:nimages
    count = count+1;
    digit = reshape(images(n,:), [28 28]);
    label = num2str(labels(n));
    count_str = num2str(count);
    fname = fullfile(file_path, label,[label '_' count_str '.png']);
    imwrite(digit, fname);
end
    
