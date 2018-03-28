% normalize_input4lenet - normalize the input matrix to be used by LeNet;

% **************************************************************************
% function [norm_data] = normalize_input4lenet(data, im_dim, num_channels, reshape_order)
%
% author: Elena Ranguelova, NLeSc
% date created: 28-03-2018
% last modification date: 
% modification details: 
%**************************************************************************
% INPUTS:
% data           input data matrix of size num_images x image_dimentions_product
% im_dim         image dimentions (original small images) vector 
% num_channels   number of color channels (?)
% reshape_order  new order of dimensions (4-elements)
%**************************************************************************
% OUTPUTS:
% norm_data     normalized (rescaled and resized) data
%**************************************************************************
% NOTES: 
%**************************************************************************
% EXAMPLES USAGE: 
% 
% see test_train_lenet_babyaishapes.m
%**************************************************************************
% REFERENCES:
%**************************************************************************
function [norm_data] = normalize_input4lenet(data, im_dim, num_channels, reshape_order)

num_images = size(data,1);

% transfer pixel values from original range to [-1 1] to satisfy the expected input
%and training paradigm of the model
norm_data =  -1 + 2.*(data - min(data))./(max(data) - min(data));
%norm_data = data.*255/ 127.5 - 1;

% reshape the data to match the requirements of the LeNet input
norm_data = permute(reshape(norm_data,[num_images, im_dim(1), im_dim(2), num_channels]),reshape_order);