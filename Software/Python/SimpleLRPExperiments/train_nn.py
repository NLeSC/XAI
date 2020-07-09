# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 18:18:41 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: In this script neural networks can be trained.
"""

import tools.data_loader
import tools.model_io
import modules
import shutil
import settings

# user init
batchsize = 25
numbIters = 20000

# load data
X, Y = tools.data_loader.load_data()

# setup neural network
nn = modules.Sequential([modules.Linear(settings.nrOfPixels, 2),
                         modules.Rect(),
                         modules.Linear(2, Y[settings.kinds[0]].shape[-1]),
                         modules.SoftMax()
                         ])

# train neural network
nn.train(X['train'],
         Y['train'],
         Xval=X['valid'],
         Yval=Y['valid'],
         batchsize=batchsize,
         iters=numbIters)

# determine training name of neural net
nnName = 'nn_' + nn.name + ('_(batchsize_{}_number_iterations_{})'
                            .format(batchsize, numbIters))

# save neural network
tools.model_io.write(nn,
                     # settings.modelPath +
                     nnName + '.txt')

# log train_nn.py that produced neural net
PythonScriptName = 'train_nn-py'
nameLogScript = 'log_' + PythonScriptName + '_for_' + nnName + '.py'
shutil.copyfile(PythonScriptName, settings.modelPath + nameLogScript)
