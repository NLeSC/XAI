# -*- coding: utf-8 -*-
"""
Created on 11/25/2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: Script for manipulating the neural network for testing.
"""

from __future__ import division
from tools import data_loader, model_io, render, data_analysis
import matplotlib.pyplot as plt
import numpy as np
import settings
import math
import mpl_toolkits.axes_grid1 as axes_grid1


# load trained neural network (nn)
nnName = 'nn_Linear_1024_2_Rect_Linear_2_2_SoftMax_(batchsize_10_number_iterations_10000).txt'
nn = model_io.read(settings.modelPath + nnName)

# I do not want to load the data every time, therefore the if statement
if 'X' not in locals():
    # load data
    X, Y = data_loader.load_data()

# load first layer weights
W1 = nn.modules[0].W
B1 = nn.modules[0].B
dim = int(W1.shape[1])
W11 = W1[:, 0]
W12 = W1[:, 1]
W11Image = render.vec2im(W11)
W12Image = render.vec2im(W12)
n = len(W11)
idxMiddleImage = int(n/2 + math.sqrt(n)/2)

# calculate innercircles to find (hidden) relationships
innerCircleSq, innerCircleTr, ring = data_analysis.inner_circles()
unionSq, unionTr = data_analysis.union_shapes()
shapeAreaOutsideRing = unionSq - innerCircleSq
weightShapeAreaOutsideRing1 = W11.dot(shapeAreaOutsideRing)
weightShapeAreaOutsideRing2 = W12.dot(shapeAreaOutsideRing)

# unique shape rotation of squares and triangles
uniqShapeRot = data_analysis.unique_shapes()
uniqShapeRotSq = uniqShapeRot['square']
uniqShapeRotTr = uniqShapeRot['triangle']

# find average weight in triangle outside ring
weightsTrOutsideRing1 = [W11.dot((1-innerCircleSq)*shape)
                         for shape in uniqShapeRotTr]
weightsTrOutsideRing2 = [W12.dot((1-innerCircleSq)*shape)
                         for shape in uniqShapeRotTr]
averWeightTrOutsideRing1 = np.mean(weightsTrOutsideRing1)
averWeightTrOutsideRing2 = np.mean(weightsTrOutsideRing2)

# modify weights
W11Mod = np.array(W11)
W11Mod[shapeAreaOutsideRing == 1.0] = 0
W11Mod[idxMiddleImage] += averWeightTrOutsideRing1
W11Mod[0] += weightShapeAreaOutsideRing1 - averWeightTrOutsideRing1
data_analysis.plot_vector_as_image(W11Mod)

"""set neural network weights to W11Mod and test accuracy afterwards

Conclusion: accuracy decreases only by 1% approx. so it is still the same nn,
I guess.
"""

nn.modules[0].W[:, 0] = W11Mod
nnPredTest = nn.forward(X['test'])
diffPredTrue = (np.argmax(nn.forward(X['test']), axis=1)
                - np.argmax(Y['test'], axis=1))
percCorrect = 100.0*np.sum(diffPredTrue == 0)/len(diffPredTrue)
print('Of the test dataset is {}% correctly predicted.'.format(percCorrect))






# # test difference for triangles after weight modification
# triangleIdxs = np.argwhere(Y['train'][:, 1] == 1)
# diffTr = np.empty((len(triangleIdxs),))
# for idx, trIdx in enumerate(triangleIdxs):
#     x = X['train'][[trIdx]]
#     diffTr[idx] = np.linalg.norm(x.dot(W11Mod) - x.dot(W11))
#
# squareIdxs = np.argwhere(Y['train'][:, 1] == 0)
# diffSq = np.empty((len(squareIdxs),))
# for idx, sqIdx in enumerate(squareIdxs):
#     x = X['train'][[sqIdx]]
#     diffSq[idx] = np.linalg.norm(x.dot(W11Mod) - x.dot(W11))
#
# plt.figure()
# plt.hist(diffSq)
# plt.hist(diffTr)
