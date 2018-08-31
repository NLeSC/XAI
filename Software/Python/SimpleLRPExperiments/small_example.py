# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 10:52:10 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: Load data, setup neural network, train neural network and test
result.
"""

import data_loader
import modules
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors
import render

# load data
if 'X' not in locals():
    X, Y = data_loader.load_data()

# setup neural network
nn = modules.Sequential([modules.Linear(32**2, 2),
                         modules.Rect(),
                         modules.Linear(2, 2),
                         modules.SoftMax()
                         ])

# train neural network
nn.train(X['train'],
         Y['train'],
         Xval=X['valid'],
         Yval=Y['valid'],
         batchsize=25,
         iters=20000)

# test result

# init figure
fig, axes = plt.subplots(figsize=(15, 4), nrows=1, ncols=3)
fig.suptitle('LRP Heatmaps for Varying Choices')
fig.tight_layout(rect=[0, 0, 1, .9])

# choose data
idx = 3
x = X['test'][[idx]]
y = Y['test'][[idx]]

# lrp evaluation
nnPred = nn.forward(x)
relevanceValues = {'nn prediction': nnPred,
                   'square': np.array([[1., 0.]]),
                   'triangle': np.array([[0., 1.]])}
lrpRelevance = {}
for idx, (key, relVal) in enumerate(relevanceValues.iteritems()):

    # find and save lrp relevance
    lrpRelevance[key] = nn.lrp(relVal, 'alphabeta', 2)

    # generate compound heatmap
    hmComp = render.hm_to_rgb(np.reshape(lrpRelevance[key], (32, 32)),
                              X=np.reshape(x, (32, 32)),
                              scaling=3,
                              shape=(),
                              sigma=2,
                              cmap='jet',
                              normalize=True)

    # plot result
    axes[idx].set_title(key)
    axes[idx].imshow(hmComp)
    axes[idx].axis('off')
