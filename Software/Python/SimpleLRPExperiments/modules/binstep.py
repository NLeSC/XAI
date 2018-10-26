# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 18:43:55 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: Contains the binary step activation layer.
See also: https://en.wikipedia.org/wiki/Heaviside_step_function
"""

import numpy as np
from module import Module

# -------------------------------
# Binary Step layer
# -------------------------------
class BinStep(Module):
    '''
    Binary Step layer
    '''
    def __init__(self):
        Module.__init__(self)
        self.layerName = 'BinStep'

    def forward(self,X):
        self.Y = 1*(X >= 0)
        return self.Y

    def backward(self,DY):
        return 0*DY

    def clean(self):
        self.Y = None

    def lrp(self,R,*args,**kwargs):
        # component-wise operations within this layer
        # ->
        # just propagate R further down.
        # makes sure subroutines never get called.
        return R