% lenet5MP_mnist_arch - defines the LeNet-5 MaxPooling architecture for MNIST
% **************************************************************************
% function [layers] = lenet5MP_mnist_arch()
%
% author: Elena Ranguelova, NLeSc
% date created: 07.03.2018
% last modification date: 
% modification details: 
%**************************************************************************
% INPUTS:
%**************************************************************************
% OUTPUTS:
% layers        the layers of the network (object of NN Toolbox)
%**************************************************************************
% NOTES: 
%**************************************************************************
% EXAMPLES USAGE: 
% 
% see train_lenet5MP_mnist.m
%**************************************************************************
% REFERENCES:
%**************************************************************************
function [layers] = lenet5MP_mnist_arch()

% layers = [
%     imageInputLayer([28 28 1])
% 
%     convolution2dLayer(5,10,'Stride',1)
%    % batchNormalizationLayer
%     reluLayer
%     maxPooling2dLayer(2,'Stride',2)
% 
%     convolution2dLayer(5,25,'Stride',1)
%     reluLayer
%     maxPooling2dLayer(2,'Stride',2)
% 
%     convolution2dLayer(4,100,'Stride',1)
%     reluLayer
%     maxPooling2dLayer(2,'Stride',2)
%      
%     convolution2dLayer(1,10,'Stride',1)
%     reluLayer
%     
%     fullyConnectedLayer(10)
%     softmaxLayer
%     classificationLayer];

layers = [
    imageInputLayer([28 28 1])
    
    convolution2dLayer(3,16,'Padding',1)
   % batchNormalizationLayer
    reluLayer
    
    maxPooling2dLayer(2,'Stride',2)
    
    convolution2dLayer(3,32,'Padding',1)
   % batchNormalizationLayer
    reluLayer
    
    maxPooling2dLayer(2,'Stride',2)
    
    convolution2dLayer(3,64,'Padding',1)
  %  batchNormalizationLayer
    reluLayer
    
    fullyConnectedLayer(10)
    softmaxLayer
    classificationLayer];
