# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 15:52:49 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: The goal of this script is to analyze the trained neural network.
"""

from tools import data_loader, model_io, render
import matplotlib.pyplot as plt
import numpy as np
import settings
import math
import mpl_toolkits.axes_grid1 as axes_grid1


# load trained neural network (nn)
nnName = nnName = 'nn_Linear_1024_2_Rect_Linear_2_2_SoftMax_(batchsize_10_number_iterations_10000).txt'
nn = model_io.read(settings.modelPath + nnName)

# I do not want to load the data every time, therefore the if statement
if 'X' not in locals():
    # load data
    X, Y = data_loader.load_data()

# inspect first linear layer
# --------------------------

W = nn.modules[0].W
B = nn.modules[0].B
dim = int(W.shape[1])

# init figure
fig = plt.figure()
grid = axes_grid1.AxesGrid(fig,
                           111,
                           nrows_ncols=(1, dim),
                           axes_pad=0.5,
                           share_all=True,
                           cbar_location="right",
                           cbar_mode="single",
                           cbar_size="15%",
                           cbar_pad="5%",)
fig.suptitle('Neural network weights images')

# plot weights
for i in range(dim):
    im = grid[i].imshow(render.vec2im(W[:, i]), cmap='jet')
    grid[i].set_title(B[i])
    grid[i].axis('off')
grid.cbar_axes[0].colorbar(im)

# inspect third layer
# -------------------

W3 = nn.modules[2].W
B3 = nn.modules[2].B

print W3
print B3


# choose data
idx = 0
x = X['test'][[idx]]
y = Y['test'][[idx]]
x[0][x[0] == np.max(x[0])] = .55
x[0][x[0] == np.min(x[0])] = .45

# nn prediction (nnPred)
nnPred = nn.forward(x)
layerOutcome = [nn.modules[0].forward(x)]
for i in range(1, len(nn.modules)):
    layerOutcome.append(nn.modules[i].forward(layerOutcome[-1]))
#print nn.modules[3].forward(nn.modules[2].forward(nn.modules[1].forward(nn.modules[0].forward(x)))) - np.array([[o[0][0]/sum(o[0]), o[0][1]/sum(o[0])]])
