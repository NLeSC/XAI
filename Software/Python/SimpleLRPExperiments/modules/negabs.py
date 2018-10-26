# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 18:43:55 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: Contains the negative absolute activation layer.
"""

import numpy as np
from module import Module

# -------------------------------
# Negative Absolute layer
# -------------------------------
class NegAbs(Module):
    '''
    Negative Absolute Layer
    '''
    def __init__(self):
        Module.__init__(self)
        self.layerName = 'NegAbs'

    def forward(self,X):
        self.X = X
        self.Y = -np.absolute(X)
        return self.Y

    def backward(self,DY):
        val = np.array(self.X)  # deep copy
        val[:] = DY
        val[val[:, 0] >= 0, 0] = -DY[val[:, 0] >= 0, 0]
        return val

    def clean(self):
        self.Y = None

    def lrp(self,R,*args,**kwargs):
        # component-wise operations within this layer
        # ->
        # just propagate R further down.
        # makes sure subroutines never get called.
        return R