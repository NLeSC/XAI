% loadMNIST2MAT - loading MNIST original data into MATLAB matricies
% **************************************************************************
% function [images,labels] = loadMNIST2MAT(fname_images,fname_labels)
%
% author: Elena Ranguelova, NLeSc
% date created: 2 March 2018
% last modification date: 
% modification details: 
%**************************************************************************
% INPUTS:
% fname_images  path to the original binary MNIST file containing images
% fname_labels  path to the original binary MNIST file containing labels
%**************************************************************************
% OUTPUTS:
% images        matrix of images of dimentions Nimages x 784 (28x28)
% labels        column vector of labels of dimentions Nimages x 1
%**************************************************************************
% NOTES: 
% uses the Stanford functions loadMNISTImages.m and loadMNISTlabesl.m
%**************************************************************************
% EXAMPLES USAGE: 
% 
% see test_script_name.m - first 2(4) cells
%**************************************************************************
% REFERENCES:
%**************************************************************************

function [images,labels] = loadMNIST2MAT(fname_images,fname_labels)

images = loadMNISTImages(fname_images);  
labels = loadMNISTLabels(fname_labels);
labels = labels';

end

