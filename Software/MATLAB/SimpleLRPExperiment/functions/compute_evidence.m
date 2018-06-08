% compute_evidence - selected statistical evidence from an LRP within a mask
% **************************************************************************
% function evidence_statistic = compute_evidence(lrp_heatmap, statistic, thresh, mask)
%
% author: Elena Ranguelova, NLeSc
% date created: 05-06-2018
% last modification date: 
% modification details: 
%**************************************************************************
% INPUTS:
% lrp_heatmap - LRP toolbox heatmap as computed by compute_lrp_heatmap.m
% statistic - string with the desired statistic name
% thresh - threshold for computing the statistic. positive number
% mask - binary mask for valid pixels. If not provided all pixels are used.
%**************************************************************************
% OUTPUTS:
% evidence_statistic - the computed evidence statistic
%**************************************************************************
% NOTES: 
%**************************************************************************
% EXAMPLES USAGE: 
% 
% see test_compute_evidence.m
%**************************************************************************
% REFERENCES:
%**************************************************************************
function evidence_statistic = compute_evidence(lrp_heatmap, statistic, thresh, mask)

if nargin<4 || isempty(mask)
    mask =  ones(size(lrp_heatmap));
end

data = lrp_heatmap.*mask;

switch statistic
    case 'NumberPositive'
        evidence_statistic = sum(data(:) >= thresh);
    case 'NumberNegative'
        evidence_statistic = sum(data(:) <= -thresh);
    case 'AverageValue'
        evidence_statistic = mean(data(:));
    case 'SizePositive'
        evidence_statistic = sum((data(:) >= thresh).*(data(:)));
    case 'SizeNegative'
        evidence_statistic = sum((data(:) <= -thresh).*(data(:)));        
    case 'DiffPosNeg'    
        evidence_statistic = sum(abs(data(:) >= thresh).*data(:));
    otherwise
        error('Unknown statistic!');
end
        
        
        

