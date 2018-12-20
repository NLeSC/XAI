# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 11:01:01 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: Bundling of some settings that can be loaded throughout.
"""

import numpy as np

# # TrianglesAndSquares
# # ===================
#
# dataName = 'TrianglesAndSquares'
# imageDimensions = (32, 32)
#
# # path locations
# dataPath = 'C:/Users/berkhout/Desktop/XAI/Data/TrianglesAndSquaresRotation/Gray/'
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
# bandsNameTest = dataName + '_bands_test_30k.mat';


# # HorizontalVersusVertical
# # ========================
#
# dataName = 'HorizontalVersusVertical'
# imageDimensions = (32, 32)
#
# # path locations
# dataPath = 'C:/Users/berkhout/Desktop/XAI/Data/HorizontalVersusVertical/'
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
# dataPath = 'C:/Users/berkhout/Desktop/XAI/Data/TrianglesAndSquaresScaleRotation/Gray/'
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


# TrianglesAndSquaresScaleRotation smaller data set
# =================================================

dataName = 'TrianglesAndSquaresScaleRotation'
imageDimensions = (64, 64)

# path locations
dataPath = 'C:/Users/berkhout/Desktop/XAI/Data/TrianglesAndSquaresScaleRotation/Gray/'
modelPath = 'models/' + dataName + '/'

# data names
kinds = ['train', 'test', 'valid']
imagesNames = {'train': dataName + '_images_train_12k.csv',
               'test': dataName + '_images_test_7k.csv',
               'valid': dataName + '_images_valid_5k.csv'}
labelsNames = {'train': dataName + '_labels_train_12k.csv',
               'test': dataName + '_labels_test_7k.csv',
               'valid': dataName + '_labels_valid_5k.csv'}


"""Some common settings are being calculated below based on values above """
nrOfPixels = np.prod(imageDimensions)  # number of pixels in the image
idxShapeColor = np.ravel_multi_index([int(x/2) for x in imageDimensions],
                                     imageDimensions)  # w.r.t. image as vector
