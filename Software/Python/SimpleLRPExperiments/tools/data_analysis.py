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
import mpl_toolkits.axes_grid1 as axes_grid1


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


def union_shapes():
    """Returns the union of all squares and triangle, respectively. """

    # check whether calling function is appropriate
    errorMessage = "Only meant for TrianglesAndSquares dataset"
    assert settings.dataName == 'TrianglesAndSquares', errorMessage

    dirPath = os.path.dirname(os.path.realpath(__file__))
    fileName = dirPath + r"\results_tools\unionShapes.pickle"

    try:
        return pickle.load(open(fileName, "rb"))
    except (OSError, IOError):

        # load data
        X, Y = data_loader.load_data()
        imageDim = len(X['train'][0])

        # init images of inner circles
        unionSq = np.zeros((imageDim,))
        unionTr = np.zeros((imageDim,))

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
                unionSq += x[0]
            else:
                # a triangle
                unionTr += x[0]

        # rescale result
        unionSq[unionSq > 0] = 1
        unionTr[unionTr > 0] = 1

        # save results
        res = (unionSq, unionTr)
        with open(fileName, 'wb') as handle:
            pickle.dump(res, handle, protocol=pickle.HIGHEST_PROTOCOL)

        # plot shapes
        plot_vector_as_image(unionSq)
        plot_vector_as_image(unionTr)

        return res


def plot_vector_as_image(vector, title=None):
    """ Plots a vector as image with colorbar. """

    fig = plt.figure()
    ax = fig.add_subplot(111)
    if title is not None:
        ax.set_title(title)
    cax = ax.matshow(render.vec2im(vector))
    fig.colorbar(cax)


def plot_multiple_vectors_as_images(dVectors, title=None):
    """ Based on dictionary dVectors, multiple vectors are
    plotted next to each other. """

    numbVectors = len(dVectors)

    # init figure
    fig = plt.figure(figsize=(15, 4))
    grid = axes_grid1.AxesGrid(fig,
                               111,
                               nrows_ncols=(1, numbVectors),
                               axes_pad=0.55,
                               share_all=True,
                               cbar_location="right",
                               cbar_mode="each",
                               cbar_size="5%",
                               cbar_pad="2%",)
    if title is not None:
        fig.suptitle(title)

    # plot vectors from dVectors
    for idx, (key, relVal) in enumerate(dVectors.iteritems()):
        im = grid[idx].imshow(render.vec2im(relVal),
                              cmap='jet')
        grid[idx].set_title(key)
        grid[idx].axis('off')
        grid.cbar_axes[idx].colorbar(im)

    # finalize figure
    if title is None:
        fig.tight_layout()
    else:
        fig.tight_layout(rect=[0, 0, 0.95, .95])


def unique_shapes():
    """Finds the unique shapes w.r.t. rotation. """

    # check whether calling function is appropriate
    errorMessage = "Only meant for TrianglesAndSquares dataset"
    assert settings.dataName == 'TrianglesAndSquares', errorMessage

    dirPath = os.path.dirname(os.path.realpath(__file__))
    fileName = dirPath + r"\results_tools\uniqueShapes.pickle"

    try:
        return pickle.load(open(fileName, "rb"), encoding='latin1')  # the encoding was needed in order to load a Python 2.7 pickle in Python 3.6. Maybe this is not necessary anymore at a later stage.
    except (OSError, IOError):

        # load data
        X, Y = data_loader.load_data()
        imageDim = len(X['train'][0])

        uniqueShapeRotSq = np.empty((0, imageDim))
        uniqueShapeRotTr = np.empty((0, imageDim))

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
                considered = any(np.equal(uniqueShapeRotSq, x[0]).all(1))
                if not considered:
                    uniqueShapeRotSq = np.vstack([uniqueShapeRotSq, x[0]])
            else:
                # a triangle
                considered = any(np.equal(uniqueShapeRotTr, x[0]).all(1))
                if not considered:
                    uniqueShapeRotTr = np.vstack([uniqueShapeRotTr, x[0]])

        # sort results
        uniqueShapeRotSq = uniqueShapeRotSq[np.argsort([min(np.flatnonzero(im)) for im in uniqueShapeRotSq])]
        uniqueShapeRotTr = uniqueShapeRotTr[np.argsort([min(np.flatnonzero(im)) for im in uniqueShapeRotTr])]

        # save results
        uniqShapeRot = {'square': uniqueShapeRotSq,
                        'triangle': uniqueShapeRotTr}
        with open(fileName, 'wb') as handle:
            pickle.dump(uniqShapeRot, handle, protocol=pickle.HIGHEST_PROTOCOL)

        return uniqShapeRot


if __name__ == "__main__":
    # can be used for testing
    results = inner_circles()
    uniqShapeRot = unique_shapes()

    for im in uniqShapeRot['triangle']:
        plot_vector_as_image(im)
