% normalize_relevance_map - normalize relevance map, so max value is 1
% **************************************************************************
% function [norm_map] = normalize_relevance_map(map)
%
% author: Elena Ranguelova, NLeSc
% date created: 05-06-2018
% last modification date: 
% modification details: 
%**************************************************************************
% INPUTS:
% map - relevance map(s) as computed by compute_lrp_heatmap.m
%**************************************************************************
% OUTPUTS:
% norm_map - normalized relevance map(s) with max value of 1
%**************************************************************************
% NOTES: 
%**************************************************************************
% EXAMPLES USAGE: 
% 
% see test_script_name.m
%**************************************************************************
% REFERENCES:
%**************************************************************************
function [norm_map] = normalize_relevance_map(map)

norm_map = map./norm(map(:), Inf);


