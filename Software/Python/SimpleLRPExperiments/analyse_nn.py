# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 15:52:49 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: The goal of this script is to analyze the trained neural network.
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

# choose some test data
idx = 0
x = X['train'][[idx]]
y = Y['train'][[idx]]
x[0][x[0] == np.max(x[0])] = .05
x[0][x[0] == np.min(x[0])] = .95
nnPred = nn.forward(x)
print nnPred
# lrpScores = nn.lrp(nnPred, 'alphabeta', 2)
# print np.sum(lrpScores)
#plt.matshow(render.vec2im(x[0] + innerCircleSq))

# inspect first linear layer
# --------------------------

W1 = nn.modules[0].W
B = nn.modules[0].B
dim = int(W1.shape[1])
W11 = W1[:, 0]
W12 = W1[:, 1]
W11Im = render.vec2im(W11)
W12Im = render.vec2im(W12)

# init figure
fig = plt.figure()
grid = axes_grid1.AxesGrid(fig,
                           111,
                           nrows_ncols=(1, dim),
                           axes_pad=0.55,
                           share_all=True,
                           cbar_location="right",
                           cbar_mode="each",
                           cbar_size="5%",
                           cbar_pad="2%",)
fig.suptitle('Neural network weights images')

# plot weights
for i in range(dim):
    im = grid[i].imshow(render.vec2im(W1[:, i]), cmap='jet')
    grid[i].set_title('W1{i}'.format(i=i+1) + ' (bias = {})'.format(round(B[i],2)))
    grid[i].axis('off')
    grid.cbar_axes[i].colorbar(im)

# calculate innercircles to find (hidden) relationships
innerCircleSq, innerCircleTr, ring = data_analysis.inner_circles()
unionSq, unionTr = data_analysis.union_shapes()
data_analysis.plot_vector_as_image(unionSq - unionTr)

def rounded_sum(x):
    return round(sum(x), 2)

print 'For W11:'
print 'Sum of outside innercircle square weights = {}'.format(rounded_sum((1-innerCircleSq)*W11))
print 'Sum of outside innercircle triangle weights = {}'.format(rounded_sum((1-innerCircleTr)*W11))
print 'Sum of innercircle square weights = {}'.format(rounded_sum(innerCircleSq*W11))
print 'Sum of innercircle triangle weights = {}'.format(rounded_sum(innerCircleTr*W11))
print 'Sum of ring weights = {}'.format(rounded_sum(ring*W11))

print 'For W12:'
print 'Sum of outside innercircle square weights = {}'.format(rounded_sum((1-innerCircleSq)*W12))
print 'Sum of outside innercircle triangle weights = {}'.format(rounded_sum((1-innerCircleTr)*W12))
print 'Sum of innercircle square weights = {}'.format(rounded_sum(innerCircleSq*W12))
print 'Sum of innercircle triangle weights = {}'.format(rounded_sum(innerCircleTr*W12))
print 'Sum of ring weights = {}'.format(rounded_sum(ring*W12))

# calculate weights inside and outside squares and triangles
weightsInSq1 = []
weightsOutsideSq1 = []
weightsSq1OutsideInnerCircle = []
weightsInSq2 = []
weightsOutsideSq2 = []
weightsSq2OutsideInnerCircle = []
weightsInTr1 = []
weightsOutsideTr1 = []
weightsInTr2 = []
weightsOutsideTr2 = []
weightsInRingTr1 = []
weightsInRingTr2 = []
weightsOutsideTrInRing1 = []
weightsOutsideTrInRing2 = []
weightsTriangleOutsideInnerCircleSquare1 = []
weightsTriangleOutsideInnerCircleSquare2 = []

for idx in range(len(X['train'])):
    x = X['train'][[idx]]
    y = Y['train'][[idx]]
    xImage = render.vec2im(x)
    halfIdx = int(math.floor(len(xImage)/2))
    xMid = xImage[halfIdx, halfIdx]
    x[0][x[0] == xMid] = 1
    x[0][np.logical_not(x[0] == 1)] = 0
    if y[0][0] == 1:
        # a square
        weightsInSq1.append(W11.dot(x[0]))
        weightsOutsideSq1.append(W11.dot(1 - x[0]))
        weightsSq1OutsideInnerCircle.append(W11.dot((1 - innerCircleSq)*x[0]))
        weightsInSq2.append(W12.dot(x[0]))
        weightsOutsideSq2.append(W12.dot(1 - x[0]))
        weightsSq2OutsideInnerCircle.append(W12.dot((1 - innerCircleSq)*x[0]))
    else:
        # a triangle
        weightsInTr1.append(W11.dot(x[0]))
        weightsOutsideTr1.append(W11.dot(1 - x[0]))
        weightsInRingTr1.append(W11.dot(x[0]*(1 - innerCircleTr)))
        weightsOutsideTrInRing1.append(W11.dot((1 - x[0])*ring))
        weightsTriangleOutsideInnerCircleSquare1.append(W11.dot((1 - innerCircleSq)*x[0]))
        weightsInTr2.append(W12.dot(x[0]))
        weightsOutsideTr2.append(W12.dot(1 - x[0]))
        weightsInRingTr2.append(W12.dot(x[0]*(1 - innerCircleTr)))
        weightsOutsideTrInRing2.append(W12.dot((1 - x[0])*ring))
        weightsTriangleOutsideInnerCircleSquare2.append(W12.dot((1 - innerCircleSq)*x[0]))

print '====================================='

print 'The average total weight of W11 inside a square is {}'.format(np.mean(weightsInSq1))
print 'The average total weight of W11 outside a square is {}'.format(np.mean(weightsOutsideSq1))
print 'The average total weight of W11 of square outside inner circle square is {}'.format(np.mean(weightsSq1OutsideInnerCircle))
print 'The average total weight of W12 inside a square is {}'.format(np.mean(weightsInSq2))
print 'The average total weight of W12 outside a square is {}'.format(np.mean(weightsOutsideSq2))
print 'The average total weight of W12 outside inner circle of a square is {}'.format(np.mean(weightsSq2OutsideInnerCircle))

print '====================================='

print 'The average total weight of W11 inside a triangle is {}'.format(np.mean(weightsInTr1))
print 'The average total weight of W11 outside a triangle is {}'.format(np.mean(weightsOutsideTr1))
print 'The average total weight of W11 of triangle in ring is {}'.format(np.mean(weightsInRingTr1))
print 'The average total weight of W11 in ring outside triangle is {}'.format(np.mean(weightsOutsideTrInRing1))
print 'The average total weight of W11 of triangle outside inner circle square is {}'.format(np.mean(weightsTriangleOutsideInnerCircleSquare1))
print 'The average total weight of W12 inside a triangle is {}'.format(np.mean(weightsInTr2))
print 'The average total weight of W12 outside a triangle is {}'.format(np.mean(weightsOutsideTr2))
print 'The average total weight of W12 of triangle in ring is {}'.format(np.mean(weightsInRingTr2))
print 'The average total weight of W12 in ring outside triangle is {}'.format(np.mean(weightsOutsideTrInRing2))
print 'The average total weight of W12 of triangle outside inner circle square is {}'.format(np.mean(weightsTriangleOutsideInnerCircleSquare2))

print '====================================='

## find how much pixels are outside the inner circle of the square
#pixelsOutsideSq = []
#pixelsOutsideTr = []
#for idx in range(len(X['train'])):
#    x = X['train'][[idx]]
#    y = Y['train'][[idx]]
#    xImage = render.vec2im(x)
#    halfIdx = int(math.floor(len(xImage)/2))
#    xMid = xImage[halfIdx, halfIdx]
#    x[0][x[0] == xMid] = 1
#    x[0][np.logical_not(x[0] == 1)] = 0
#    if y[0][0] == 1:
#        # a square
#        pixelsOutsideSq.append((W11.dot(x[0] - innerCircleSq)))
#    else:
#        # a triangle
#        pixelsOutsideTr.append((W11.dot(x[0] - innerCircleTr)))


# inspect third layer
# -------------------

W3 = nn.modules[2].W
B3 = nn.modules[2].B

print W3
print B3


# Some old code below


# nn prediction (nnPred)
nnPred = nn.forward(x)
layerOutcome = [nn.modules[0].forward(x)]
for i in range(1, len(nn.modules)):
    layerOutcome.append(nn.modules[i].forward(layerOutcome[-1]))