# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 17:14:16 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: Elaboration of the strategy of the neural network.
"""

from __future__ import division
from sympy import *
from tools import data_loader, model_io, render, data_analysis
import matplotlib.pyplot as plt
import numpy as np
import settings
import math
import mpl_toolkits.axes_grid1 as axes_grid1
import itertools
import pickle


# load trained neural network (nn)
nnName = 'nn_Linear_1024_2_Rect_Linear_2_2_SoftMax_(batchsize_10_number_iterations_10000).txt'
nn = model_io.read(settings.modelPath + nnName)

# I do not want to load the data every time, therefore the if statement
if 'X' not in locals():
    # load data
    X, Y = data_loader.load_data()

# first linear layer
W1 = nn.modules[0].W
B = nn.modules[0].B
dim = int(W1.shape[1])
W11 = W1[:, 0]
W12 = W1[:, 1]
W11Im = render.vec2im(W11)
W12Im = render.vec2im(W12)

# third linear layer
W3 = nn.modules[2].W
B3 = nn.modules[2].B

# calculate innercircles to find (hidden) relationships
innerCircleSq, innerCircleTr, ring = data_analysis.inner_circles()

print 'For W11:'
print 'Sum of outside innercircle square weights = {}'.format(sum((1-innerCircleSq)*W11))
print 'Sum of outside innercircle triangle weights = {}'.format(sum((1-innerCircleTr)*W11))
print 'Sum of innercircle square weights = {}'.format(sum(innerCircleSq*W11))
print 'Sum of innercircle triangle weights = {}'.format(sum(innerCircleTr*W11))
print 'Sum of ring weights = {}'.format(sum(ring*W11))

print 'For W12:'
print 'Sum of outside innercircle square weights = {}'.format(sum((1-innerCircleSq)*W12))
print 'Sum of outside innercircle triangle weights = {}'.format(sum((1-innerCircleTr)*W12))
print 'Sum of innercircle square weights = {}'.format(sum(innerCircleSq*W12))
print 'Sum of innercircle triangle weights = {}'.format(sum(innerCircleTr*W12))
print 'Sum of ring weights = {}'.format(sum(ring*W12))

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
        weightsInTr2.append(W12.dot(x[0]))
        weightsOutsideTr2.append(W12.dot(1 - x[0]))
        weightsInRingTr2.append(W12.dot(x[0]*(1 - innerCircleTr)))

print '====================================='

print 'The average total weight of W11 inside a square is {}'.format(np.mean(weightsInSq1))
print 'The average total weight of W11 outside a square is {}'.format(np.mean(weightsOutsideSq1))
print 'The average total weight of W11 outside inner circle of a square is {}'.format(np.mean(weightsSq1OutsideInnerCircle))
print 'The average total weight of W12 inside a square is {}'.format(np.mean(weightsInSq2))
print 'The average total weight of W12 outside a square is {}'.format(np.mean(weightsOutsideSq2))
print 'The average total weight of W12 outside inner circle of a square is {}'.format(np.mean(weightsSq2OutsideInnerCircle))

print '====================================='

print 'The average total weight of W11 inside a triangle is {}'.format(np.mean(weightsInTr1))
print 'The average total weight of W11 outside a triangle is {}'.format(np.mean(weightsOutsideTr1))
print 'The average total weight of W11 of triangle in ring is {}'.format(np.mean(weightsInRingTr1))
print 'The average total weight of W12 inside a triangle is {}'.format(np.mean(weightsInTr2))
print 'The average total weight of W12 outside a triangle is {}'.format(np.mean(weightsOutsideTr2))
print 'The average total weight of W12 of triangle in ring is {}'.format(np.mean(weightsInRingTr2))

print '====================================='


# for W11
meanWeightsInSq1 = np.mean(weightsInSq1)
meanWeightsInTr1 = np.mean(weightsInTr1)
weightsOutsideSq1 = np.mean(weightsOutsideSq1)
weightsOutsideTr1 = np.mean(weightsOutsideTr1)

# for W12
meanWeightsInSq2 = np.mean(weightsInSq2)
meanWeightsInTr2 = np.mean(weightsInTr2)
weightsOutsideSq2 = np.mean(weightsOutsideSq2)
weightsOutsideTr2 = np.mean(weightsOutsideTr2)

# analyze neural network with sympy
# =================================

x, y = symbols('x y')  # color nr. shape and background, resp.

# linear layer 1

# in case image is a square
outputLayer1Sq = [Max(meanWeightsInSq1*x + weightsOutsideSq1*y + B[0], 0),
                  Max(meanWeightsInSq2*x + weightsOutsideSq2*y + B[0], 0)]
outputLayer1Sq = Matrix(1, 2, outputLayer1Sq)

# in case image is a square
outputLayer1Tr = [Max(meanWeightsInTr1*x + weightsOutsideTr1*y + B[0], 0),
                  Max(meanWeightsInTr2*x + weightsOutsideTr2*y + B[0], 0)]
outputLayer1Tr = Matrix(1, 2, outputLayer1Tr)

# linear layer 3
W3Sympy = Matrix(W3)
B3Sympy = Matrix(1, 2, B3)
outputLayer3Sq = outputLayer1Sq*W3Sympy + B3Sympy  # square
outputLayer3Tr = outputLayer1Tr*W3Sympy + B3Sympy  # triangle
outputLayer3SqRounded = N(simplify(outputLayer3Sq), 1)
outputLayer3TrRounded = N(simplify(outputLayer3Tr), 1)

# sympy output
sympyOutputSq = Matrix(1,
                       2,
                       [exp(outputLayer3Sq[0])/(exp(outputLayer3Sq[0]) + exp(outputLayer3Sq[1])),
                        exp(outputLayer3Sq[1])/(exp(outputLayer3Sq[0]) + exp(outputLayer3Sq[1]))])
sympyOutputTr = Matrix(1,
                       2,
                       [exp(outputLayer3Tr[0])/(exp(outputLayer3Tr[0]) + exp(outputLayer3Tr[1])),
                        exp(outputLayer3Tr[1])/(exp(outputLayer3Tr[0]) + exp(outputLayer3Tr[1]))])
sympyOutputSqRounded = N(simplify(sympyOutputSq), 2)
sympyOutputTrRounded = N(simplify(sympyOutputTr), 2)

# test how accurate the sympy representation of the neural network is
# ===================================================================

# TEST 1
# ======

"""Description: Choose a test image and see what the impact is of different
colors as given in colorVals for the image and background.
"""

# get a test image (im) with known classification
imageIdx = 0
im = X['train'][[imageIdx]]
classification = Y['train'][[imageIdx]]

# determine index of a color in shape and background
idxShapeColor = np.ravel_multi_index([16, 16], (32, 32))
idxBackgroundColor = 0

# init
colorVals = np.arange(0, 1, .1)
numbVals = len(colorVals)
results = np.empty((len(colorVals), len(colorVals)))

for idx, (xColor, yColor) in enumerate(itertools.product(colorVals, colorVals)):

    # set color in test image
    im[0][im[0] == im[0][idxShapeColor]] = xColor
    im[0][im[0] == im[0][idxBackgroundColor]] = yColor

    # determine output of neural network (nn)
    nnPred = nn.forward(im)

#    # determine output of sympy representation
#    outputLayer3Subs = np.array(outputLayer3Sq.subs([(x, xColor), (y, yColor)])).astype(np.float64)
#    sympyPred = np.exp(outputLayer3Subs)/np.sum(np.exp(outputLayer3Subs))
    if classification[0][0] == 1:
        # square
        sympyPred = np.array(sympyOutputSq.subs([(x, xColor), (y, yColor)])).astype(np.float64)
    else:
        # triangle
        sympyPred = np.array(sympyOutputTr.subs([(x, xColor), (y, yColor)])).astype(np.float64)

    # save and print results
    results[np.unravel_index(idx, (numbVals, numbVals))] = round(np.linalg.norm(nnPred - sympyPred), 2)
    print idx, round(xColor, 1), round(yColor, 1), round(results[np.unravel_index(idx, (numbVals, numbVals))], 2), np.round(nnPred, 2), np.round(sympyPred, 2)

# TEST 2
# ======

"""Description: Find the accuracy over the test data set with the neural
network and the sympy representation of the neural network based on an
average.
"""

# make predictions with neural network and evaluate result
nnPredTest = nn.forward(X['test'])
diffPredTrue = (np.argmax(nn.forward(X['test']), axis=1)
                - np.argmax(Y['test'], axis=1))
percCorrect = 100.0*np.sum(diffPredTrue == 0)/len(diffPredTrue)
print('Of the test dataset is {}% correctly predicted.'.format(percCorrect))

try:
    with open('results\sympyPredTest.pickle', 'rb') as handle:
        sympyPredTest = pickle.load(handle)
except (OSError, IOError):

    print 'Warning: the following may take some time...'

    # make predictions with sympy representation
    sympyPredTest = np.array(nnPredTest)  # will be overwritten, do not worry
    for idx, im in enumerate(X['test']):

        print 100.0*idx/len(X['test'])  # progress report

        classification = Y['test'][[idx]]
        xColor = im[idxShapeColor]
        yColor = im[idxBackgroundColor]

        if classification[0][0] == 1:
            # square
            sympyPred = np.array(sympyOutputSq.subs([(x, xColor), (y, yColor)])).astype(np.float64)
        else:
            # triangle
            sympyPred = np.array(sympyOutputTr.subs([(x, xColor), (y, yColor)])).astype(np.float64)

        sympyPredTest[idx] = sympyPred[0]

    # save result
    with open('results\sympyPredTest.pickle', 'wb') as handle:
        pickle.dump(sympyPredTest, handle, protocol=pickle.HIGHEST_PROTOCOL)

# compare neural network and sympy representation
meanDiff = np.mean((nnPredTest - sympyPredTest)[:, 0])
stdDiff = np.std((nnPredTest - sympyPredTest)[:, 0])
print 'Results comparison neural network and sympy representation predictions:'
print 'The average difference of square probability is: {}'.format(meanDiff)
CIWidth = 2.0*stdDiff/math.sqrt(len(nnPredTest))
print 'With 95% confidence interval: [{}, {}]'.format(meanDiff - CIWidth,
                                                      meanDiff + CIWidth)
print 'Conclusion: the sympy is a really good representative of the neural network.'
print 'In other words: analyzing the sympy representation gives some intuition about the strategy.'

# save sympy representation
with open('results\sympyRepresentationOutputLayer3SqNN.pickle', 'wb') as handle:
    handle.write(pickle.dumps(outputLayer3SqRounded))
