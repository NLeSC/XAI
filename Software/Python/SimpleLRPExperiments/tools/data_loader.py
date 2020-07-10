# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 11:16:18 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: Data loading functions can be found here.
"""

from scipy.io import loadmat
from sklearn.model_selection import train_test_split
import settings
import numpy as np
import time
import pandas as pd
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

    if settings.imagesNames is None:
        # assuming a .npz file to be loaded (meant for CountingCirclesDiffRaddiVar)
        # warning: settings.kinds are hardcoded below 'as usual'

        print('Start data loading ...')

        # load data
        data = np.load(settings.dataPath + settings.dataset_name)
        data_size = len(data['images'])
        images = data['images'].reshape(data_size, settings.nrOfPixels)  # ensure that it becomes vectors instead of matrices
        labels = reshape_labels_to_vectors(data['labels'].reshape(data_size, 1))

        # split data
        Data['train'], X_valid_train, Labels['train'], y_valid_train = train_test_split(images, labels, test_size=0.6, random_state=42)
        Data['valid'], Data['test'], Labels['valid'], Labels['test'] = train_test_split(X_valid_train, y_valid_train, test_size=0.5, random_state=42)

        print('Data loaded!')

        return Data, Labels

    for kind in settings.kinds:

        print('Start loading {} data'.format(kind))
        startTime = time.time()

        pathData = os.path.join(settings.dataPath, settings.imagesNames[kind])     
        pathLabels = os.path.join(settings.dataPath, settings.labelsNames[kind])

        try:
            Data[kind] = loadmat(pathData)[kind + '_images']
            Labels[kind] = reshape_labels_to_vectors(loadmat(pathLabels)[kind + '_labels'])
        except KeyError:
            # TODO: Define dict keys corresponding to the datasets in settings.py and refer to those
            try:
                # in order to load the HorizontalVersusVertical data
                Data[kind] = loadmat(pathData)['Images']
                Labels[kind] = reshape_labels_to_vectors(loadmat(pathLabels)['Labels'])
            except KeyError:
                # in order to load the CountingCircles data
                Data[kind] = loadmat(pathData)['P']
                Labels[kind] = reshape_labels_to_vectors(loadmat(pathLabels)['C_actual'])
        except ValueError:
            # in case of a csv file
            # TODO: Maybe use pandas' HDF5 for a speed boost?
            Data[kind] = pd.read_csv(pathData, header=None).values
            Labels[kind] = reshape_labels_to_vectors(pd.read_csv(pathLabels, header=None).values)
            
        elapsedTime = time.time() - startTime
        print('Loaded {} data in {}s'.format(kind, elapsedTime))

    return Data, Labels


def reshape_labels_to_vectors(Labels):
    """Reshape label data into binary values.

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
