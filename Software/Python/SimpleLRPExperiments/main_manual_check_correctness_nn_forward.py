# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 15:52:49 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: This script manually checks whether the forward calculations of
the small neural network in file

nn_Linear_1024_2_Rect_Linear_2_2_SoftMax_(batchsize_25_number'
          '_iterations_1000).txt

are correctly implemented in the LRP toolbox.

The conclusion is that the LRP calculates the prediction as expected.

Warning: ugly code inside :-).
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

# load weights of first and third layer
W = nn.modules[0].W
B = nn.modules[0].B
W3 = nn.modules[2].W
B3 = nn.modules[2].B

# choose data
idx = 0
x = X['test'][[idx]]
y = Y['test'][[idx]]
x[0][x[0] == np.max(x[0])] = 0
x[0][x[0] == np.min(x[0])] = 1

# nn prediction (nnPred)
nnPred = nn.forward(x)

# test whether neural network forward is what is expected

# first layer
print 'First layer difference between output nn and own calculations:'
print nn.modules[0].forward(x) - (x.dot(W) + B)

def maxNonNegative(x):
    return max(x, 0)

# second layer
print 'Second layer difference between output nn and own calculations:'
print nn.modules[1].forward(nn.modules[0].forward(x)) - np.array([map(maxNonNegative, (x.dot(W) + B)[0])])

# third layer
print 'Third layer difference between output nn and own calculations:'
print nn.modules[2].forward(nn.modules[1].forward(nn.modules[0].forward(x))) - (np.array([map(maxNonNegative, (x.dot(W) + B)[0])]).dot(W3) + B3)

# fourth layer
print 'Fourth layer difference between output nn and own calculations:'
o = np.exp(np.array([map(maxNonNegative, (x.dot(W) + B)[0])]).dot(W3) + B3)
print nn.modules[3].forward(nn.modules[2].forward(nn.modules[1].forward(nn.modules[0].forward(x)))) - np.array([[o[0][0]/sum(o[0]), o[0][1]/sum(o[0])]])