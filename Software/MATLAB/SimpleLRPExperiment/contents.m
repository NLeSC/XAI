% contents.m- contents of directory ...\XAI\SimpleLRPExperiment
%
% topic: Studying the usefulness of the LRP Toolbox heatmaps when
% explaining circles vs sqaures vs triangles simple shape classification 
% author: Elena Ranguelova, NLeSc
% date: March/April 2018
%
%**************************************************************************
% functions
%**************************************************************************
% amat_loader - function to load data from the amat format
% normalize_input4lenet - normalize the input matrix to be used by LeNet
% reshape_labels - reshaping the labels to fit LRP toolbox format
% lenet_arch - LeNet CNN architecture using LRP Toolbox
%**************************************************************************
% test_scripts
%**************************************************************************
% test_amat_loader - testing script for the amat format loader
% train_lenet_babyaishapes.m - testing the training of LeNet5 CNN on the BabaAIShapes dataset
% test_lenet_babyaishapes.m - testing the performance of the LeNet5 CNN on the BabaAIShapes dataset
%**************************************************************************
% misc
%**************************************************************************
% config.m - setting configurable parameters