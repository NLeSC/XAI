% reshape_labels - reshaping the labels to fit LRP toolbox format
% **************************************************************************
% function [reshaped_labels] = reshape_labels(labels)
%
% author: Elena Ranguelova, NLeSc
% date created: 28.032018
% last modification date: 24.05.2018
% modification details: quick hack to handle 2 of 3 possible labels
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

max_label = max(labels(:));
num_uniq_el = numel(unique(labels));

if max_label + 1 > num_uniq_el % only 3>2!
    num_classes = max_label;
    index(labels==0)= 1;
    index(labels==2)= 2;
    index =  index';
else
    num_classes = num_uniq_el;
    index = labels+1;
end
%index = labels+1;
reshaped_labels = zeros(size(labels,1),num_classes); %numel(unique(labels)));
reshaped_labels(sub2ind(size(reshaped_labels),1:size(reshaped_labels,1),index')) = 1;