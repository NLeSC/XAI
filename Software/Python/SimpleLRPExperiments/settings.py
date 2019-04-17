# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 11:01:01 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: Bundling of some settings that can be loaded throughout.
"""

import numpy as np
from os.path import dirname

# roots of project and data folder
projectRootPath = dirname(dirname(dirname(dirname(__file__))))
dataRootPath = projectRootPath + '/Data'


# # TrianglesAndSquares
# # ===================
#
# dataName = 'TrianglesAndSquares'
# imageDimensions = (32, 32)
#
# # path locations
# dataPath = dataRootPath + '/TrianglesAndSquaresRotation/Gray/'
# modelPath = 'models/' + dataName + '/'
#
# # data names
# kinds = ['train', 'test', 'valid']
# imagesNames = {'train': dataName + '_images_train_50k.mat',
#                'test': dataName + '_images_test_30k.mat',
#                'valid': dataName + '_images_valid_20k.mat'}
# labelsNames = {'train': dataName + '_labels_train_50k.mat',
#                'test': dataName + '_labels_test_30k.mat',
#                'valid': dataName + '_labels_valid_20k.mat'}
# bandsNameTest = dataName + '_bands_test_30k.mat'


# # HorizontalVersusVertical
# # ========================
#
# dataName = 'HorizontalVersusVertical'
# imageDimensions = (32, 32)
#
# # path locations
# dataPath = dataRootPath + '/HorizontalVersusVertical/'
# modelPath = 'models/' + dataName + '/'
#
# # data names
# kinds = ['train', 'test', 'valid']
# imagesNames = {'train': 'Images_train.mat',
#                'test': 'Images_test.mat',
#                'valid': 'Images_validation.mat'}
# labelsNames = {'train': 'Labels_train.mat',
#                'test': 'Labels_test.mat',
#                'valid': 'Labels_validation.mat'}


# # TrianglesAndSquaresScaleRotation
# # ================================
#
# dataName = 'TrianglesAndSquaresScaleRotation'
# imageDimensions = (64, 64)
#
# # path locations
# dataPath = dataRootPath + 'TrianglesAndSquaresScaleRotation/Gray/'
# modelPath = 'models/' + dataName + '/'
#
# # data names
# kinds = ['train', 'test', 'valid']
# imagesNames = {'train': dataName + '_images_train_50k.csv',
#                'test': dataName + '_images_test_30k.csv',
#                'valid': dataName + '_images_valid_20k.csv'}
# labelsNames = {'train': dataName + '_labels_train_50k.csv',
#                'test': dataName + '_labels_test_30k.csv',
#                'valid': dataName + '_labels_valid_20k.csv'}


## TrianglesAndSquaresScaleRotation smaller data set
## =================================================
#
#dataName = 'TrianglesAndSquaresScaleRotation'
#imageDimensions = (64, 64)
#
## path locations
#dataPath = dataRootPath + '/TrianglesAndSquaresScaleRotation/Gray/'
#modelPath = 'models/' + dataName + '/'
#
## data names
#kinds = ['train', 'test', 'valid']
#imagesNames = {'train': dataName + '_images_train_12k.csv',
#               'test': dataName + '_images_test_7k.csv',
#               'valid': dataName + '_images_valid_5k.csv'}
#labelsNames = {'train': dataName + '_labels_train_12k.csv',
#               'test': dataName + '_labels_test_7k.csv',
#               'valid': dataName + '_labels_valid_5k.csv'}


# # Counting (possibly overlappinng) circles data set
# # =================================================
#
# dataName = 'CountingCircles'
# imageDimensions = (100, 100)
#
# # path locations
# dataPath = dataRootPath + '/' + dataName + '/'
# modelPath = 'models/' + dataName + '/'
#
# # data names
# kinds = ['train', 'test', 'valid']
# imagesNames = {'train': 'P_train.mat',
#                'test': 'P_test.mat',
#                'valid': 'P_validation.mat'}
# labelsNames = {'train': 'C_actual_train.mat',
#                'test': 'C_actual_test.mat',
#                'valid': 'C_actual_validation.mat'}


# Counting non-overlappinng objects (circles) data set
# =================================================

dataName = 'Distinct_Objects'
imageDimensions = (100, 100)

# path locations
dataPath = dataRootPath + '/' + dataName + '/'
modelPath = 'models/' + dataName + '/'

 # data names
kinds = ['train', 'test', 'valid']
imagesNames = {'train': 'P_distinct_train.mat',
               'test': 'P_distinct_test.mat',
               'valid': 'P_distinct_validate.mat'}
labelsNames = {'train': 'C_distinct_actual_train.mat',
               'test': 'C_distinct_actual_test.mat',
               'valid': 'C_distinct_actual_validate.mat'}

"""Some common settings are being calculated below based on values above """
nrOfPixels = np.prod(imageDimensions)  # number of pixels in the image
idxShapeColor = np.ravel_multi_index([int(x/2) for x in imageDimensions],
                                     imageDimensions)  # w.r.t. image as vector
