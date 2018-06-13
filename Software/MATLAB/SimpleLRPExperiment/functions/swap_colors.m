% swap_colors - Swaps the background and foreground color in an image 
% described by a vector v.
% **************************************************************************
% function [vSwapped] = swap_colors(v)
%
% author: Elena Ranguelova, NLeSc, Joost Berkhout, CWI
% date created: 13-6-2018
% last modification date: 
% modification details: 
%**************************************************************************
% INPUTS:
% v - a vector describing the image consisting of 2 colors.
%**************************************************************************
% OUTPUTS:
% vSwapped - a vector describing the image with swapped colors
%**************************************************************************
% NOTES: 
%**************************************************************************
% EXAMPLES USAGE: 
%**************************************************************************
% REFERENCES:
%**************************************************************************
function [vSwapped] = swap_colors(v)

% init
uniqVal = unique(v);
vSwapped = zeros(size(v));

if size(uniqVal) > 2
    error('The function is written for 2 unique values.')
end
    
vSwapped(v == uniqVal(1)) = uniqVal(2);
vSwapped(v == uniqVal(2)) = uniqVal(1);
