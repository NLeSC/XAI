# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 11:16:18 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: Data loading functions can be found here.
"""

from scipy.io import loadmat
import settings
import numpy as np


def load_data():
    """Loads data based upon the settings in settings.py.

    Parameters
    ----------
    None (all information comes from settings.py)

    Returns
    -------
    X : dict
      A dictionary that contains the different datasets for the different
      kinds as given in settings.py.

    Y : dict
      Gives the labels corresponding to the data in X.

    Notes
    -----
    """

    # init
    X = {}
    Y = {}

    for kind in settings.kinds:
        pathX = settings.dataPath + settings.imagesNames[kind]
        pathY = settings.dataPath + settings.labelsNames[kind]
        X[kind] = loadmat(pathX)[kind + '_images']
        Y[kind] = reshape_labels_to_vectors(loadmat(pathY)[kind + '_labels'])

    return X, Y


def reshape_labels_to_vectors(Y):
    """Loads data based upon the settings in settings.py.

    Parameters
    ----------
    Y : np.array (n x 1)
      Array with image labels.

    Returns
    -------
    reshapedY : np.array np.array (n x uniqueElements(Y))
      Reshaped version of Y with binary values.

    Notes
    -----
    """

    # init
    uniqVals = np.unique(Y)
    reshapedY = np.zeros((len(Y), len(uniqVals)))

    for idx, uniqVal in enumerate(uniqVals):
        reshapedY[(Y == uniqVal)[:, 0], idx] = 1

    return reshapedY


if __name__ == "__main__":
    print 'Is it a module or a script?'
