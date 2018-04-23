% lenet5_maxpool_arch - LeNet5 max pool CNN architecture using LRP Toolbox
% **************************************************************************
% function [net] = lenet_arch()
%
% author: Elena Ranguelova, NLeSc
% date created: 23-04-2018
% last modification date:
% modification details: 
%**************************************************************************
% INPUTS:
%**************************************************************************
% OUTPUTS:
% lenet         lenet Sequential architecture object as defined in LRP Toolbox
%**************************************************************************
% NOTES: 
% 
%**************************************************************************
% EXAMPLES USAGE: 
% 
% see test_train_lenet_babyaishapes
%**************************************************************************
% REFERENCES:
%**************************************************************************
function [net] = lenet5_maxpool_arch()

%model network according to LeNet-5 architecture
net = modules.Sequential({
                            modules.Convolution([5 5 1 10],[1 1]),...
                            modules.Rect(),...
                            modules.MaxPool([2 2],[2 2]),...
                            modules.Convolution([5 5 10 25],[1 1]),...
                            modules.Rect(),...
                            modules.MaxPool([2 2],[2 2]),...
                            modules.Convolution([4 4 25 100],[1 1]),...
                            modules.Rect(),...
                            modules.MaxPool([2 2],[2 2]),...
                            modules.Convolution([1 1 100 3],[1 1]),...
                            modules.Flatten()
                            });
