# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 11:01:01 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: Bundling of some settings that can be loaded throughout.
"""

# path locations
dataPath = 'C:/Users/berkhout/Desktop/XAI/Data/TrianglesAndSquaresRotation/Gray/'
modelPath = 'models/TrianglesAndSquares/'

# data names
kinds = ['train', 'test', 'valid']
imagesNames = {'train': 'TrianglesAndSquares_images_train_50k.mat',
               'test': 'TrianglesAndSquares_images_test_30k.mat',
               'valid': 'TrianglesAndSquares_images_valid_20k.mat'}
labelsNames = {'train': 'TrianglesAndSquares_labels_train_50k.mat',
               'test': 'TrianglesAndSquares_labels_test_30k.mat',
               'valid': 'TrianglesAndSquares_labels_valid_20k.mat'}
bandsNameTest = 'TrianglesAndSquares_bands_test_30k.mat';
