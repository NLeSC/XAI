# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 11:01:01 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: Bundling of some settings that can be loaded throughout.
"""

# TrianglesAndSquares
# ===================

dataName = 'TrianglesAndSquares'

# path locations
dataPath = 'C:/Users/berkhout/Desktop/XAI/Data/TrianglesAndSquaresRotation/Gray/'
modelPath = 'models/' + dataName + '/'

# data names
kinds = ['train', 'test', 'valid']
imagesNames = {'train': dataName + '_images_train_50k.mat',
               'test': dataName + '_images_test_30k.mat',
               'valid': dataName + '_images_valid_20k.mat'}
labelsNames = {'train': dataName + '_labels_train_50k.mat',
               'test': dataName + '_labels_test_30k.mat',
               'valid': dataName + '_labels_valid_20k.mat'}
bandsNameTest = dataName + '_bands_test_30k.mat';


## HorizontalVersusVertical
## ===================
#
#dataName = 'HorizontalVersusVertical'
#
## path locations
#dataPath = 'C:/Users/berkhout/Desktop/XAI/Data/HorizontalVersusVertical/'
#modelPath = 'models/' + dataName + '/'
#
## data names
#kinds = ['train', 'test', 'valid']
#imagesNames = {'train': 'Images_train.mat',
#               'test': 'Images_test.mat',
#               'valid': 'Images_validation.mat'}
#labelsNames = {'train': 'Labels_train.mat',
#               'test': 'Labels_test.mat',
#               'valid': 'Labels_validation.mat'}
