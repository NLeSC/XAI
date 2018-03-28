% reshape_labels - reshaping the labels to fit LRP toolbox format
% **************************************************************************
% function [reshaped_labels] = reshape_labels(labels)
%
% author: Elena Ranguelova, NLeSc
% date created: 28.032018
% last modification date: 
% modification details: 
%**************************************************************************
% INPUTS:
% labels        a vector of single label per training esample
%**************************************************************************
% OUTPUTS:
% reshaped_labels [num_samples,classes] label matrix as required by LRP toolbox
%**************************************************************************
% NOTES: 
%**************************************************************************
% EXAMPLES USAGE: 
% 
% see test_train_lenet_babyaishapes.m
%**************************************************************************
% REFERENCES:
%**************************************************************************
function [reshaped_labels] = reshape_labels(labels)


index = labels+1;
reshaped_labels = zeros(size(labels,1),numel(unique(labels)));
reshaped_labels(sub2ind(size(reshaped_labels),1:size(reshaped_labels,1),index')) = 1;