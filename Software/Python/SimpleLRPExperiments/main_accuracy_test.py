# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 10:52:10 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: Load a trained neural network from train_nn.py and test how
accurate the neural network is on the test dataset.
"""

from tools import data_loader, model_io, render
import matplotlib.pyplot as plt
import numpy as np
import settings

# load trained neural network (nn)
nnName = 'nn_Linear_1024_1_Rect_Linear_1_2_SoftMax_(batchsize_10_number_iterations_10000).txt'
#nnName = 'nn_Linear_1024_2_Rect_Linear_2_2_SoftMax_(batchsize_10_number_iterations_10000).txt'
nn = model_io.read(settings.modelPath + nnName)

# I do not want to load the data every time, therefore the if statement
if 'X' not in locals():
    # load data
    X, Y = data_loader.load_data()

# make predictions and evaluate result
nnPredTest = nn.forward(X['test'])
diffPredTrue = (np.argmax(nn.forward(X['test']), axis=1)
                - np.argmax(Y['test'], axis=1))
percCorrect = 100.0*np.sum(diffPredTrue == 0)/len(diffPredTrue)
print('Of the test dataset is {}% correctly predicted.'.format(percCorrect))