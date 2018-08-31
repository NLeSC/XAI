# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 11:16:18 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: Data loading functions can be found here.
"""

from scipy.io import loadmat
import settings
import numpy as np

DATA_PATH = 'C:/Users/berkhout/Desktop/XAI/Data/TrianglesAndSquaresRotation/Gray/'


def load_data():

    # init
    X = {}
    Y = {}

    for kind in settings.kinds:
        pathX = DATA_PATH + settings.imagesNames[kind]
        pathY = DATA_PATH + settings.labelsNames[kind]
        X[kind] = loadmat(pathX)[kind + '_images']
        Y[kind] = reshape_labels_to_vectors(loadmat(pathY)[kind + '_labels'])

    return X, Y


def reshape_labels_to_vectors(Y):

    uniqVals = np.unique(Y)
    reshapedY = np.zeros((len(Y), len(uniqVals)))
    for idx, uniqVal in enumerate(uniqVals):
        reshapedY[(Y == uniqVal)[:, 0], idx] = 1
    return reshapedY


if __name__ == "__main__":
    print 'Is it a module or a script?'
