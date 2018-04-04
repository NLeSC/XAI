% lenet3_maxpool_arch - LeNet5 max pool CNN architecture using LRP Toolbox
% **************************************************************************
% function [net] = lenet3_pool_arch()
%
% author: Elena Ranguelova, NLeSc
% date created: 04-04-2018
% last modification date:
% modification details: 
%**************************************************************************
% INPUTS:
%**************************************************************************
% OUTPUTS:
% lenet         lenet Sequential architecture object as defined in LRP Toolbox
%**************************************************************************
% NOTES: 
% Code taken and modified from lenet5_sumpool_arch
%**************************************************************************
% EXAMPLES USAGE: 
% 
% see test_train_lenet_babyaishapes
%**************************************************************************
% REFERENCES:
%**************************************************************************
function [net] = lenet3_maxpool_arch()

%model network according to LeNet architecture
net = modules.Sequential({
                            modules.Convolution([7 7 1 10],[1 1]),...
                            modules.Rect(),...
                            modules.MaxPool([4 4],[2 2]),...
                            modules.Convolution([5 5 10 25],[1 1]),...
                            modules.Rect(),...
                            modules.MaxPool([8 8],[2 2]),...
                            modules.Convolution([1 1 25 3],[1 1]),...
                            modules.Flatten(),...
                            modules.SoftMax()
                            });
