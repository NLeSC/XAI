# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 20:19:44 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: In this script the LRP can be studied for a user chosen image.
"""

from tools import data_loader, model_io, render, data_analysis
import numpy as np
import settings

# init
imageIdx = 12  # index of the image that will be loaded

# load trained neural network (nn)
nnName = 'nn_Linear_4096_6_Rect_Linear_6_2_SoftMax_(batchsize_10_number_iterations_10000).txt'
# nnName = 'nn_Linear_10000_4_Rect_Linear_4_3_SoftMax_(batchsize_10_number_iterations_100000).txt'
# nnName = 'nn_Linear_10000_4_Tanh_Linear_4_4_SoftMax_(batchsize_10_number_iterations_1000).txt'
# nnName = 'nn_Linear_10000_4_Rect_Linear_4_4_SoftMax_(batchsize_10_number_iterations_100).txt'
# nnName = 'nn_Linear_4096_4_Rect_Linear_4_2_SoftMax_(batchsize_10_number_iterations_20000).txt'
# nnName = 'nn_Linear_1024_2_Rect_Linear_2_2_SoftMax_(batchsize_10_number_iterations_10000).txt'
nn = model_io.read(settings.modelPath + nnName)

# I do not want to load the data every time, therefore the if statement
if 'X' not in locals():
    # load data
    X, Y = data_loader.load_data()

# LRP test regarding strategy
# ===========================

# get a test image (im) with known classification
im = X['test'][[imageIdx]]
classification = Y['test'][[imageIdx]]
data_analysis.plot_vector_as_image(im, title=str(classification))

# init neural network
nnPred = nn.forward(im)

print('True classifictions is {}'.format(classification))
print('Predictions is {}'.format(nnPred))

# calculate lrpRelevance scores for manually set relevance values
relevanceValues = {'nn prediction': nnPred,
                   # '1 circles': np.array([[1., 0., 0.]]),
                   # '2 circles': np.array([[0., 1., 0.]]),
                   # '3 circles': np.array([[0., 0., 1.]])
                   # 'square': np.array([[1., 0.]]),
                   # 'triangle': np.array([[0., 1.]])
                   }
lrpRelevance = {}
for idx, (key, relVal) in enumerate(relevanceValues.items()):

    # find and save lrp relevance
    lrpRelevance[key] = nn.lrp(relVal, 'alphabeta', 2)

# simple plot of weights without normalization
titlePlot = ('LRP Heatmaps for Varying Choices (neural net prediction = {})'
             .format(np.round(nnPred, 2)[0]))
lrpRelevance['originalImage'] = im[0]  # also plot original image
data_analysis.plot_multiple_vectors_as_images(lrpRelevance,
                                              titlePlot)
