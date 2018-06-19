% short_relu_arch - Short relu architecture using LRP Toolbox
% **************************************************************************
% function [net] = short_relu_arch()
%
% author: Joost Berkhout, CWI
% date created: 10-06-2018
% last modification date:
% modification details: 
%**************************************************************************
% INPUTS:
%**************************************************************************
% OUTPUTS:
% lenet         lenet Sequential architecture object as defined in LRP Toolbox
%**************************************************************************
% NOTES: 
% Inspired by https://github.com/VigneshSrinivasan10/interprettensor.
% Idea is that maybe a simpler net gives more intuition via LRP in line
% with LRP demo at:
% https://lrpserver.hhi.fraunhofer.de/handwriting-classification
%**************************************************************************
% EXAMPLES USAGE: 
% 
% see test_train_lenet_babyaishapes
%**************************************************************************
% REFERENCES:
%**************************************************************************
function [net] = short_relu_arch()

% short_relu
% ----------
% net = modules.Sequential({
%                             modules.Linear(32^2, 36^2),...
%                             modules.Rect(),...
%                             modules.Linear(36^2, 36^2),...
%                             modules.Rect(),...
%                             modules.Linear(36^2, 2),...
%                             modules.Flatten(),...
%                             modules.SoftMax()
%                             });

% min_short_relu
% --------------
% net = modules.Sequential({
%                             modules.Linear(32^2, 3^2),...
%                             modules.Linear(3^2, 2),...
%                             });

% two_layer_short_relu
% --------------------
net = modules.Sequential({
                            modules.Linear(32^2, 3),...
                            modules.Rect(),...
                            modules.Linear(3, 2),...
                            modules.SoftMax()
                            });