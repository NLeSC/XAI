# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 10:52:10 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: Load a trained neural network from train_nn.py and put lrp to
the test. Please check whether the settings in settings.py are correct.
"""

from tools import data_loader, model_io, render, data_analysis
import matplotlib.pyplot as plt
import numpy as np
import settings
import math


# load trained neural network (nn)
nnName = 'nn_Linear_1024_2_Rect_Linear_2_2_SoftMax_(batchsize_10_number_iterations_10000).txt'
nn = model_io.read(settings.modelPath + nnName)

# I do not want to load the data every time, therefore the if statement
if 'X' not in locals():
    # load data
    X, Y = data_loader.load_data()

# test result

# init figure
fig, axes = plt.subplots(figsize=(15, 4), nrows=1, ncols=3)
fig.suptitle('LRP Heatmaps for Varying Choices')
fig.tight_layout(rect=[0, 0, 1, .9])

# choose data
idx = 0
x = X['test'][[idx]]
y = Y['test'][[idx]]

# lrp evaluation
nnPred = nn.forward(x)
relevanceValues = {'nn prediction': nnPred,
                   'square': np.array([[1., 0.]]),
                   'triangle': np.array([[0., 1.]])}
lrpRelevance = {}
for idx, (key, relVal) in enumerate(relevanceValues.items()):

    # find and save lrp relevance
    lrpRelevance[key] = nn.lrp(relVal, 'alphabeta', 2)

    # generate compound heatmap
    hmComp, R = render.hm_to_rgb(render.vec2im(lrpRelevance[key]),
                                 X=render.vec2im(x),
                                 scaling=3,
                                 shape=(),
                                 sigma=2,
                                 cmap='jet',
                                 normalize=True)

    # plot result
    axes[idx].set_title(key + ': ' + str(np.round(relVal[0], 2)))
    img = axes[idx].imshow(hmComp)
    axes[idx].axis('off')
    fig.colorbar(img, ax=axes[idx])

# just a simple plot of weights without normalization
titlePlot = 'LRP Heatmaps for Varying Choices (Without Scaling at SoftMax Layer)'
data_analysis.plot_multiple_vectors_as_images(lrpRelevance,
                                              titlePlot)
