# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 18:18:41 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: In this script neural networks can be trained.
"""

import data_loader
import modules
import model_io

# user init
batchsize = 25
numbIters = 1000

# load data
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
         batchsize=batchsize,
         iters=numbIters)

# determine name of test
trainingName = 'nn_' + nn.name + ('_(batchsize_{}_number_iterations_{})'
                                  .format(batchsize, numbIters))

# save neural network
model_io.write(nn, 'models/TrianglesAndSquares/' + trainingName + '.txt')



