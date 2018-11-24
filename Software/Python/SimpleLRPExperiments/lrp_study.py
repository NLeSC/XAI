# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 20:19:44 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: In this script the LRP can be studied for a user chosen image.
"""

from tools import data_loader, model_io, render, data_analysis
import numpy as np
import settings

# choose color of loaded picture
imageIdx = 0
shapeColor = .5
backgroundColor = .6

# load trained neural network (nn)
nnName = 'nn_Linear_1024_2_Rect_Linear_2_2_SoftMax_(batchsize_10_number_iterations_10000).txt'
nn = model_io.read(settings.modelPath + nnName)

# I do not want to load the data every time, therefore the if statement
if 'X' not in locals():
    # load data
    X, Y = data_loader.load_data()

# LRP test regarding strategy
# ===========================

# determine index of a color in shape and background
idxShapeColor = np.ravel_multi_index([16, 16], (32, 32))
idxBackgroundColor = 0

# get a test image (im) with known classification
im = X['train'][[imageIdx]]
classification = Y['train'][[imageIdx]]

# determine colors in test image
shapeColorIm = im[0][idxShapeColor]
backgroundColorIm = im[0][idxBackgroundColor]

# set colors in test image
imOwnColors = np.array(im)
imOwnColors[0][im[0] == shapeColorIm] = shapeColor
imOwnColors[0][im[0] == backgroundColorIm] = backgroundColor

data_analysis.plot_vector_as_image(imOwnColors)

# init neural network
nnPred = nn.forward(imOwnColors)

# calculate lrpRelevance scores
relevanceValues = {'nn prediction': nnPred,
                   'square': np.array([[1., 0.]]),
                   'triangle': np.array([[0., 1.]])}
lrpRelevance = {}
for idx, (key, relVal) in enumerate(relevanceValues.iteritems()):

    # find and save lrp relevance
    lrpRelevance[key] = nn.lrp(relVal, 'alphabeta', 2)

# simple plot of weights without normalization
titlePlot = ('LRP Heatmaps for Varying Choices (neural net prediction = {})'
             .format(np.round(nnPred, 2)[0]))
lrpRelevance['originalImage'] = imOwnColors[0]  # also plot original image
data_analysis.plot_multiple_vectors_as_images(lrpRelevance,
                                              titlePlot)