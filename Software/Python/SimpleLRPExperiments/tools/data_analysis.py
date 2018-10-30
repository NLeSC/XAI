# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:07:19 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: This module contains function in order to analyse the data.
"""

import pickle
import settings
import numpy as np
import render
import math
import data_loader
import matplotlib.pyplot as plt
import os


def inner_circles():
    """Returns the inner circles of squares and triangles plus ring, resp. """

    # check whether calling function is appropriate
    errorMessage = "Only meant for TrianglesAndSquares dataset"
    assert settings.dataName == 'TrianglesAndSquares', errorMessage

    dirPath = os.path.dirname(os.path.realpath(__file__))
    fileName = dirPath + r"\results_tools\innerCircles.pickle"

    try:
        return pickle.load(open(fileName, "rb"))
    except (OSError, IOError):

        # load data
        X, Y = data_loader.load_data()
        imageDim = len(X['train'][0])

        # init images of inner circles
        innerCircleSq = np.ones((imageDim,))
        innerCircleTr = np.ones((imageDim,))

        for idx in range(len(X['train'])):

            x = X['train'][[idx]]
            y = Y['train'][[idx]]

            # find xMid in the middle of the image of x
            xImage = render.vec2im(x)
            halfIdx = int(math.floor(len(xImage)/2))
            xMid = xImage[halfIdx, halfIdx]

            # set shape color to 1 and background color to 0
            x[0][x[0] == xMid] = 1
            x[0][np.logical_not(x[0] == 1)] = 0

            if y[0][0] == 1:
                # a square
                innerCircleSq = innerCircleSq*x[0]
            else:
                # a triangle
                innerCircleTr = innerCircleTr*x[0]

        # find ring
        ring = innerCircleSq - innerCircleTr

        # save results
        res = (innerCircleSq, innerCircleTr, ring)
        with open(fileName, 'wb') as handle:
            pickle.dump(res, handle, protocol=pickle.HIGHEST_PROTOCOL)

        # plot shapes
        plot_vector_as_image(innerCircleSq)
        plot_vector_as_image(innerCircleTr)
        plot_vector_as_image(ring)

        return res


def plot_vector_as_image(vector):
    """ Quickly plots a vector as image. """
    plt.matshow(render.vec2im(vector))


if __name__ == "__main__":
    # can be used for testing
    results = inner_circles()
