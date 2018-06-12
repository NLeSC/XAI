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

% model network according to short relu architecture
net = modules.Sequential({
                            modules.Linear(32^2, 36^2),...
                            modules.Rect(),...
                            modules.Linear(36^2, 36^2),...
                            modules.Rect(),...
                            modules.Linear(36^2, 2),...
                            modules.Flatten(),...
                            modules.SoftMax()
                            });
