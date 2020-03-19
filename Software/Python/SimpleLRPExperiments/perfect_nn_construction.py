# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 10:21:32 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: In this script, we attempt of constructing the perfect neural
network.
"""

from __future__ import division
from tools import data_loader, model_io, render, data_analysis
import matplotlib.pyplot as plt
import numpy as np
import settings
import math
import mpl_toolkits.axes_grid1 as axes_grid1


nnName = 'nn_Linear_1024_1_NegAbs_BinStep_Linear_1_2_SoftMax_(batchsize_10_number_iterations_10000).txt'
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

# calculate innercircles to find (hidden) relationships
innerCircleSq, innerCircleTr, ring = data_analysis.inner_circles()

# lets create the perfect nn (Wi = weight matrix layer i, bi = bias layer i)
W1 = np.array(ring)/sum(ring)  # set ring values as initialization
W1[int(len(W1) / 2 + 16)] = -1
W1 = W1.reshape((len(W1), 1))
B1 = np.array([0])
#W1Image = render.vec2im(W1)
#plt.matshow(W1Image)
W2 = np.array([[1, -1]])
B2 = np.array([0, 1])

# set weights in neural networks
nn.modules[0].B = B1
nn.modules[0].W = W1
nn.modules[3].B = B2
nn.modules[3].W = W2

# make predictions and evaluate result
nnPredTest = nn.forward(X['test'])
diffPredTrue = (np.argmax(nn.forward(X['test']), axis=1)
                - np.argmax(Y['test'], axis=1))
percCorrect = 100.0*np.sum(diffPredTrue == 0)/len(diffPredTrue)
print('Of the test dataset is {}% correctly predicted by the perfect neural network.'.format(percCorrect))