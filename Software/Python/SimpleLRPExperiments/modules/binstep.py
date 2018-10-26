# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 18:43:55 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: Contains the binary step activation layer.

See also: https://en.wikipedia.org/wiki/Heaviside_step_function

Two options are implemented: the true bin step function and an
analytical approximation as given on Wikipedia. The idea of the
analytical approximation is that its derivative exists, making it
more smooth.

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
        self.K = 100000  # large constant
        self.eps = 1.0/self.K  # very small constant

    def forward(self,X):

        self.X = X

#        # analytic approximation of the bin step function
#        self.Y = .5 + .5*np.tanh(self.K*X)
#        return self.Y

         # true bin step function:
        self.Y = 1*(X >= -self.eps)
        return self.Y

    def backward(self,DY):

#        # analytic approximation of the bin step function
#        return DY*.5*self.K*(1.0-self.Y**2)

        # true bin step function:
        return 0*DY

    def clean(self):
        self.Y = None

    def lrp(self,R,*args,**kwargs):
        # component-wise operations within this layer
        # ->
        # just propagate R further down.
        # makes sure subroutines never get called.
        return R