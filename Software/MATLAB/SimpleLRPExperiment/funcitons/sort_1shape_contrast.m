% sort_1shape_contrast - sort images of a shape by contrast between BG and FG
% **************************************************************************
% function [sorted_1shape_images, shape_index, sort_1shape_index] = ...
%        sort_1shape_contrast(input_images, input_labels, shape_label, bg_point,fg_point, unique_flag)
%
% author: Elena Ranguelova, NLeSc
% date created: 11-04-2018
% last modification date: 09-05-2018
% modification details: added unique flag
%**************************************************************************
% INPUTS:
% input_images   matrix containing BabyAIShapes images all shapes
% input_labels   column vector of size num_images x 1 containing the shape labels 
% shape_label    the label of the shape: 0-square, 1- circle, 2- triangle
% bg_point       indicies (row,col) of a point belonging to the BG
% fg_point       indicies (row,col) of a point belonging to the FG (shape)
% unique_flag    flag indicating weather tho retun only unque values
%**************************************************************************
% OUTPUTS:
% sorted_1shape_images  the matrix of images for the chosen shape 
%                sorted line-wise first according to BG
%                gray level, then by FG (object) gray level 
% shape_index    the index indicating the spesific shapes
% sort_index     the original index of the images order after the sorting
%**************************************************************************
% NOTES: uses sort_contrast function
%**************************************************************************
% EXAMPLES USAGE: 
% 
% see test_sort_1shape_contrast.m
%**************************************************************************
% REFERENCES:
%**************************************************************************
function [sorted_1shape_images, shape_index, sort_1shape_index] = ...
        sort_1shape_contrast(input_images, input_labels, shape_label, bg_point,fg_point, unique_flag)
    
% select the images of the givel shape
shape_index = find(input_labels == shape_label);
input_1shape_images = input_images(shape_index,:);

% sort the images of that shape
[sorted_1shape_images, sort_1shape_index] = sort_contrast(input_1shape_images, bg_point, fg_point, unique_flag);


