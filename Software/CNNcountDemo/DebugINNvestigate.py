#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 18:44:43 2020

@author: elena
"""

# based on the DebuggingModel1SingleImageSingleMethod.ipynb
# %% Imports
import warnings
warnings.simplefilter('ignore')

import imp
import numpy as np
import os.path
import matplotlib.pyplot as plt

from tensorflow.keras import backend as K
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
from keras.models import load_model

import innvestigate
import innvestigate.utils as iutils
mnistutils = imp.load_source("utils_mnist", "/home/elena/eStep/XAI/Software/innvestigate/examples/utils_mnist.py")

from CNNcount import shape_images as si

# %% data

# filename for loading the data from the NPZ files (NumPy compressed)
same_shape_same_radius_fname = "/home/elena/eStep/XAI/Data/CountingShapes/circles_same_radius_60k.npz"
# input image dimensions and number of classes
img_rows, img_cols = 64, 64
num_classes = 3

# load the set of images with the same type and same radius and split to train and test subsets
if os.path.isfile(same_shape_same_radius_fname): # already generated- just load
    print ("The file containing images of the same shape (circle) with same radius already exist!")
    # load from NPZ file for display
    images_train, _, images_test, _, _, labels_test = si.load_split_data(same_shape_same_radius_fname)
    
    
    if K.image_data_format() == 'channels_first':
        images_train = images_train.reshape(images_train.shape[0], 1, img_rows, img_cols)
        images_test = images_test.reshape(images_test.shape[0], 1, img_rows, img_cols)
    print("Size of train data: ", np.shape(images_train))
    print("Size of test data: ", np.shape(images_test), "and labels: ", np.shape(labels_test))
else: # missing data
    print ("The file containing images of the same shape (circle) with same radius does not exist!")
    print("Use the GenerateShapeImages notebook to generate the experimental data.") 

# %% chose a random image for testing

nim = len(labels_test)
ind=int(np.random.randint(1,nim))
img=images_test[ind,:,:]
img=np.reshape(img,(64,64))
label=labels_test[ind]
plt.imshow(img,cmap='binary')
plt.title('ind=%d n=%d' % (ind,label))
plt.show()

# %% model
# filename for model saving
same_shape_same_radius_model_fname = "/home/elena/eStep/XAI/Data/CountingShapes/model_circles_same_radius.h5"
# load the trained model
model = load_model(same_shape_same_radius_model_fname) 
print("Loaded model from disk")
print("Model summary")
model.summary()

# %% Pattern Net analyzer loading

model_wo_sm = iutils.keras.graph.model_wo_softmax(model)
path_to_analyzers = "/home/elena/eStep/XAI/Data/CountingShapes/Analyzers"
fname = os.path.join(path_to_analyzers, 'pattern.net2.npz')
PatternNet_analyzer = innvestigate.create_analyzer("pattern.net", model_wo_sm, pattern_type = "relu")

if os.path.isfile(fname):
    print("Analyzer exists. Loading...")
    PatternNet_analyzer = PatternNet_analyzer.load_npz(fname)
else:
    print("Analyzer doesn't exist. Training and [Saving]...")
    # Some analyzers require training.
    PatternNet_analyzer.fit(images_train, batch_size=200, verbose=1)
    PatternNet_analyzer.save_npz(fname)

# %% Pattern Net analysis
image = img[np.newaxis, :, :, np.newaxis].astype(np.float32)
analysis = PatternNet_analyzer.analyze(image)
    
# Display
plt.imshow(analysis.squeeze(), cmap='seismic', interpolation='nearest')
plt.show()
