% normalize_relevance_map - normalize relevance map to be in the range [0 1]
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
% norm_map - normalized relevance map(s) to be in the range [0 1]
%**************************************************************************
% NOTES: Maybe use LRP toolbox render.hm_to_rgb instead!
%**************************************************************************
% EXAMPLES USAGE: 
% 
% see test_normalize_relevance_map.m
%**************************************************************************
% REFERENCES:
%**************************************************************************
function [norm_map] = normalize_relevance_map(map)

%norm_map = map./norm(map(:), Inf);
min_map = min(map(:));
max_map = max(map(:));

norm_map = (map-min_map)./(max_map - min_map);


