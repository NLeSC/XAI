% sort_contrast - sort a set of images on contrast between BG and FG (object)
% **************************************************************************
% function [output_mages, sort_index] = sort_contrast(input_images, bg_point, fg_point)
%
% author: Elena Ranguelova, NLeSc
% date created: 06-04-2018
% last modification date: 11-04-2018
% modification details: correct sorting algorithm, added sorted index output
%**************************************************************************
% INPUTS:
% input_images_matrix  matrix containing BabyAIShapes returned by amat_loader
%                of one or more shapes
% bg_point       indicies (row,col) of a point belonging to the BG
% fg_point       indicies (row,col) of a point belonging to the FG (shape)
%**************************************************************************
% OUTPUTS:
% output_images  the matrix sorted line-wise first according to BG
%                gray level, then by FG (object) gray level
% sort_index     the original index of the images order after the sorting
%**************************************************************************
% NOTES: 
%**************************************************************************
% EXAMPLES USAGE: 
% 
% see test_sort_contrast.m
%**************************************************************************
% REFERENCES:
%**************************************************************************
function [output_images, sort_index] = sort_contrast(input_images, bg_point, fg_point)

% number of images
num_images = size(input_images,1);

% initializaitons
output_images = zeros(size(input_images));
shape_images = zeros(num_images, 32, 32);
bg_values = zeros(1,num_images);
fg_values = zeros(1,num_images);


% indicies of a BG and FG points
fg_row = fg_point(1); fg_col = fg_point(2);
bg_row = bg_point(1); bg_col = bg_point(2);

% collect row vectors of BG and FG values
for ind = 1:num_images
    shape_images(ind,:,:) = reshape(input_images(ind,:),32,32);
    bg_values(ind) = shape_images(ind, bg_row, bg_col);
    fg_values(ind) = shape_images(ind, fg_row, fg_col);
end
clear shape_images

% create combined vector from the BG and FG values for sorting
combined_values = bg_values * 1000 + fg_values;

% sort 
[~,sort_index] = sort(combined_values);

% construct output matrix by using sorted indicies
for ind =  1:num_images
    output_images(ind,:) = input_images(sort_index(ind),:);
end



