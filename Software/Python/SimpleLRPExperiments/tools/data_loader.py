# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 11:16:18 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: Data loading functions can be found here.
"""

from scipy.io import loadmat
import settings
import numpy as np
import os


def load_data():
    """Loads data based upon the settings in settings.py.

    Parameters
    ----------
    None (all information comes from settings.py)

    Returns
    -------
    Data : dict
      A dictionary that contains the different datasets for the different
      kinds (train/test/...) as given in settings.py.

    Labels : dict
      Gives the labels corresponding to the data in Data.

    Notes
    -----
    """

    # init
    Data = {}
    Labels = {}

    for kind in settings.kinds:
        pathData = os.path.join(settings.dataPath, settings.imagesNames[kind])       
        pathLabels = os.path.join(settings.dataPath, settings.labelsNames[kind])
        Data[kind] = loadmat(pathData)[kind + '_images']
        Labels[kind] = reshape_labels_to_vectors(loadmat(pathLabels)[kind + '_labels'])

    return Data, Labels


def reshape_labels_to_vectors(Labels):
    """Loads data based upon the settings in settings.py.

    Parameters
    ----------
    Labels : np.array (n x 1)
      Array with image labels.

    Returns
    -------
    reshapedLabels : np.array np.array (n x uniqueElements(Labels))
      Reshaped version of Labels with binary values.

    Notes
    -----
    """

    # init
    uniqVals = np.unique(Labels)
    reshapedLabels = np.zeros((len(Labels), len(uniqVals)))

    for idx, uniqVal in enumerate(uniqVals):
        reshapedLabels[(Labels == uniqVal)[:, 0], idx] = 1

    return reshapedLabels


if __name__ == "__main__":
    print('Is it a module or a script?')
