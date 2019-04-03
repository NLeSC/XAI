# -*- coding: utf-8 -*-
"""
Created on 4/3/2019

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: Inspection of the weights of the neural net.
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


# load trained neural network (nn)
nnName = 'nn_Linear_10000_4_Rect_Linear_4_3_SoftMax_(batchsize_10_number_iterations_100000).txt'
nn = model_io.read(settings.modelPath + nnName)

# load weights and biases of linear layers
linearModules = [module for module in nn.modules if 'Linear' in module.layerName]
weightsLinMods = {module.layerName: module.W for module in linearModules}
biasLinMods = {module.layerName: module.B for module in linearModules}

# weightsLinMods.pop(linearModules[-1].layerName)
data_analysis.plot_images(weightsLinMods, 'Weights for ' + nnName)
