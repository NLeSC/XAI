% sum_pixels_evidence_2class - agreggated pixel evidence for, against or neutral for 2 classes
% **************************************************************************
% function [evidence_same, evidence_diff] = sum_pixel_evidence_2class(true_labels, ...
%                           rel_matrix_class1, rel_matrix_class2, eps)
%
% author: Elena Ranguelova, NLeSc
% date created: 30-05-2018
% last modification date:
% modification details:
%**************************************************************************
% INPUTS:
% true_labels   the true labels for a given image (test) set
% rel_matrix1/2 the relevance matrix for the selected class
% eps           the value defining relevance threshold
%**************************************************************************
% OUTPUTS:
% evidence_same/diff  structure arrays  with aggregated evidence for a
%                     selected class - the same of different respectively.
%                      Fields: True label, Nr positive pixels,
%                      Nr Negative pixels, Nr neutral pixels
%**************************************************************************
% NOTES:
%**************************************************************************
% EXAMPLES USAGE:
%
% see test_sum_pixel_evidence_2class.m
%**************************************************************************
% REFERENCES:
%**************************************************************************
function [evidence_same, evidence_diff] = sum_pixels_evidence_2class(true_labels, ...
    rel_matrix_class1, rel_matrix_class2, eps)

% number of images
num_images = length(true_labels);
im_dim = size(rel_matrix_class1,2);

% unique classes
classes = unique(true_labels);
class1 = classes(1); class2 = classes(2);

% fill in the evidence structure
for it = 1:num_images
    label = true_labels(it);
    evidence_same(it).true_label = label;
    evidence_diff(it).true_label = label;
    
    sum_pos_eps1  =  sum(rel_matrix_class1(it,:)>eps);
    sum_pos_eps2 = sum(rel_matrix_class2(it,:)>eps);
    sum_neg_eps1 = sum(rel_matrix_class1(it,:)<-eps);
    sum_neg_eps2 = sum(rel_matrix_class2(it,:)<-eps);
    
    switch label
        case class1
            evidence_same(it).num_pos_pixels = sum_pos_eps1; %#ok<*AGROW>
            evidence_diff(it).num_pos_pixels = sum_pos_eps2;
            evidence_same(it).num_neg_pixels = sum_neg_eps1;            
            evidence_diff(it).num_neg_pixels = sum_neg_eps2;            
            evidence_same(it).num_neut_pixels = im_dim - (sum_pos_eps1 + sum_neg_eps1);
            evidence_diff(it).num_neut_pixels = im_dim - (sum_pos_eps2 + sum_neg_eps2);
        case class2
            evidence_same(it).num_pos_pixels = sum_pos_eps2; %#ok<*AGROW>
            evidence_diff(it).num_pos_pixels = sum_pos_eps1;
            evidence_same(it).num_neg_pixels = sum_neg_eps2;
            evidence_diff(it).num_neg_pixels = sum_neg_eps1;
            evidence_same(it).num_neut_pixels = im_dim - (sum_pos_eps2 + sum_neg_eps2);
            evidence_diff(it).num_neut_pixels = im_dim - (sum_pos_eps2 + sum_neg_eps2);
            
    end
end

