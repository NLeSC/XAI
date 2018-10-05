# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 10:52:10 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: Load a trained neural network from train_nn.py and put lrp to
the test. Please check whether the settings in settings.py are correct.
"""

from tools import data_loader, model_io, render
import matplotlib.pyplot as plt
import numpy as np
import settings
import math
import mpl_toolkits.axes_grid1 as axes_grid1


# load trained neural network (nn)
nnName = 'nn_Linear_1024_3_Rect_Linear_3_2_SoftMax_(batchsize_10_number_iterations_100000).txt'

nn = model_io.read(settings.modelPath + nnName)

# I do not want to load the data every time, therefore the if statement
if 'X' not in locals():
    # load data
    X, Y = data_loader.load_data()

# test result

# choose data for lrp
idx = 1
x = X['test'][[idx]]
y = Y['test'][[idx]]

# lrp evaluation
nnPred = nn.forward(x)
relevanceValues = {'nn prediction': nnPred,
                   'square': np.array([[1., 0.]]),
                   'triangle': np.array([[0., 1.]])}
lrpRelevance = {}
hmComp = {}
for idx, (key, relVal) in enumerate(relevanceValues.iteritems()):

    # find and save lrp relevance
    lrpRelevance[key] = nn.lrp(relVal, 'alphabeta', 2)

    # generate compound heatmap
    hmComp[key], R = render.hm_to_rgb(render.vec2im(lrpRelevance[key]),
                                 X=render.vec2im(x),
                                 scaling=3,
                                 shape=(),
                                 sigma=2,
                                 cmap='jet',
                                 normalize=True)

#    hmComp[key] = render.vec2im(lrpRelevance[key])



# init figure
fig = plt.figure()
grid = axes_grid1.AxesGrid(fig,
                           111,
                           nrows_ncols=(1, 3),
                           axes_pad=0.5,
                           cbar_location="right",
                           cbar_mode="single",
                           cbar_size="15%",
                           cbar_pad="5%",)
fig.suptitle('LRP Heatmaps for Varying Choices')
#fig.tight_layout(rect=[0, 0, 1, .9])

for idx, (key, relVal) in enumerate(relevanceValues.iteritems()):

    # plot result
    grid[idx].set_title(key + ': ' + str(np.round(relVal[0], 2)))
    img = grid[idx].imshow(hmComp[key], cmap='jet')#, interpolation='nearest')
    grid[idx].axis('off')
#    fig.colorbar(img, ax=axes[idx])

grid.cbar_axes[0].colorbar(img)
