 # -*- coding: utf-8 -*-
"""
Created on 6/29/2020

Author: Joost Berkhout (VU, email: j2.berkhout@vu.nl)

Description: Applies Deep k-nearest neighbors to the triangle and squares data.
"""

import math
import os.path
import shutil

import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.models import load_model
from tensorflow.keras import initializers
import tensorflow.keras

import tools.data_loader
import tools.data_analysis
import settings

np.random.seed(0)

# init
epochs = 3
batch_size = 10
retrain_existing_model = True
k = 10  # number of nearest neighbors to consider per layer

# load data
X, Y = tools.data_loader.load_data()

# training

# Initialize the constructor
model = Sequential()

# Add an input layer
model.add(Dense(units=2,
                kernel_initializer=initializers.RandomNormal(stddev=1.0*settings.nrOfPixels**(-.5)),
                input_shape=(settings.nrOfPixels,),
                name='Dense1_2'))

model.add(Activation('relu', name='relu'))  # for testing: can be replaced by adding activation in previous Dense

# Add an output layer
model.add(Dense(units=Y[settings.kinds[0]].shape[-1],
                kernel_initializer=initializers.RandomNormal(stddev=1.0*settings.nrOfPixels**(-.5)),
                name='Dense2_2'))

model.add(Activation('softmax', name='softmax'))

model.compile(loss='mean_squared_error',
              optimizer='adam',
              metrics=['accuracy'])

# determine training name of neural net
layer_names = '_'.join([l.name for l in model.layers])
model_name = ('nn_keras_tf2_' + layer_names +
              '_(epochs_{}_batchsize_{})'.format(epochs, batch_size))
model_loc = settings.modelPath + model_name + ".hdf5"

if os.path.isfile(model_loc) and not retrain_existing_model:
    model = load_model(model_loc)
else:
    print('Start training ' + model_name + '.')

    train_history = model.fit(X['train'],
                              Y['train'],
                              validation_data=(X['valid'], Y['valid']),
                              epochs=epochs,
                              batch_size=batch_size,
                              verbose=1)

    model.save(model_loc)

    # log main_DkNN.py that produced neural net
    script_name = 'main_DkNN.py'
    nameLogScript = 'log_' + script_name + '_for_' + model_name + '.py'
    shutil.copyfile(script_name, settings.modelPath + nameLogScript)

# evaluate model on test data
YPred = model.predict(X['test'])
pred_errs = np.average(np.argmax(Y['test'], 1) == np.argmax(YPred, 1))
print(f'The model accuracy on test data is {pred_errs}')

# apply DkNN
extractor = tensorflow.keras.Model(inputs=model.inputs,
                                   outputs=[model.inputs] + [l.output for l in model.layers])
train_features = extractor(X['train'])
test_image_features = extractor(X['test'][0:1, :])

# plot datapoints after first label
fig, ax = plt.subplots()
train_labels = np.argmax(Y['train'], 1)
label_symbols = ['s', '^']
for label_idx in np.unique(train_labels):
    filter = train_labels == label_idx
    ax.scatter(train_features[1].numpy()[filter][:, 0],
               train_features[1].numpy()[filter][:, 1],
               marker=label_symbols[label_idx],
               alpha=0.3)
ax.legend()
ax.grid(True)










# # use GradCAM
# # model.summary()
# img = X['test'][0:1,:]
# y_img = np.argmax(Y['test'], 1)[0]
# data = (np.array([img]), y_img)
# #
# from tf_explain.core.grad_cam import GradCAM
# import tf_explain.utils.display
# explainer = GradCAM()
# # Compute GradCAM on VGG16
# grid = explainer.explain(
#     data, model, class_index=1, layer_name='dense_1'
# )
# explainer.save(grid, ".", "grad_cam.png")
#
# import matplotlib.pyplot as plt
# imgplot = plt.imshow(grid.reshape(1,32,32,3)[0])
tools.data_analysis.plot_vector_as_image(X['train'][0:1,:], f'label = {Y["train"][ 0:1, :]}')
# tools.data_analysis.plot_vector_as_image(grid[0], 'test')
