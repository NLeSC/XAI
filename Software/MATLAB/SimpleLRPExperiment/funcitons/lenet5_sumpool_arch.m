% lenet5_sumpool_arch - LeNet5 sum pool CNN architecture using LRP Toolbox
% **************************************************************************
% function [net] = lenet_arch()
%
% author: Elena Ranguelova, NLeSc
% date created: 29-03-2018
% last modification date:04-04-2018
% modification details: Renaming
%**************************************************************************
% INPUTS:
%**************************************************************************
% OUTPUTS:
% lenet         lenet Sequential architecture object as defined in LRP Toolbox
%**************************************************************************
% NOTES: 
% Code taken directly from the LRP Toolbox v.1.2: cnn_training_test.m
%**************************************************************************
% EXAMPLES USAGE: 
% 
% see test_train_lenet_babyaishapes
%**************************************************************************
% REFERENCES:
%**************************************************************************
function [net] = lenet5_sumpool_arch()

%model network according to LeNet-5 architecture
net = modules.Sequential({
                            modules.Convolution([5 5 1 10],[1 1]),
                            modules.Rect(),
                            modules.SumPool([2 2],[2 2])
                            modules.Convolution([5 5 10 25],[1 1]),
                            modules.Rect(),
                            modules.SumPool([2 2],[2 2]),
                            modules.Convolution([4 4 25 100],[1 1]),
                            modules.Rect(),
                            modules.SumPool([2 2],[2 2]),
                            modules.Convolution([1 1 100 3],[1 1]),
                            modules.Flatten()
                            });
