# -*- coding: utf-8 -*-
"""
Created on 7/5/2020

Author: Joost Berkhout (VU, email: j2.berkhout@vu.nl)

Description: Utilities of Deep k-nearest neighbors (DkNN).
"""

import math
import numpy as np
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import render

class DkNN:
    """
    Deep k-nearest neighbors (DkNN) implementation for analysis.

    Attributes
    ----------
    extractor : keras.model
        Keras model with as output all layers we are interested in.

    X : np.array
        Data to compare the input against.

    Y : np.array
        Labels of data to compare the input against.

    k : int
        Number of neighbors to consider

    X_input : np.array
        Input data to the neural network to apply DkNN to (e.g., an image).

    Y_input : optional
        Label of input data.
    """

    def __init__(self, extractor, X, Y, k, X_input, Y_input, Y_input_predict):

        # store init data
        self.extractor = extractor
        self.X = X['train']
        self.Y = Y['train']
        self.k = k
        self.X_input = X_input
        self.Y_input = Y_input
        self.Y_input_predict = Y_input_predict

        # calculate data and input through neural network
        self.data_features = self.extractor(self.X)
        self.input_features = self.extractor(self.X_input)

        # find nearest neighbors of all layers
        self.NN_layers = self.find_nearest_neighb_all_layers()

    def find_nearest_neighb_all_layers(self):

        NN_layers = []

        for layer_idx in range(len(self.extractor.layers)):

            # find nearest neighbors
            neigh = NearestNeighbors(n_neighbors=self.k, metric='euclidean')
            neigh.fit(self.data_features[layer_idx])
            distances, indices = neigh.kneighbors(self.input_features[layer_idx])

            # save data
            data_layer = {'layer name': self.extractor.layers[layer_idx].name,
                          'distances': distances[0],
                          'indices': indices[0],
                          'X': self.X[indices[0]],
                          'Y': self.Y[indices[0]],
                          }
            NN_layers.append(data_layer)

        return NN_layers

    def plot_NN_layer(self, layer_idx, nr_to_plot=None):
        """Plots of nr_to_plot nearest neighbors (NN) of a layer in a grid. """

        if nr_to_plot is None:
            nr_to_plot = self.k + 1  # plot input data and all neighbors found

        # init data
        NN = self.NN_layers[layer_idx]
        confirmation_perc_NN = 100*np.mean(np.argmax(NN['Y'], 1) == np.argmax(self.Y_input_predict, 1)[0])

        # init figure
        nr_of_rows = math.ceil(math.sqrt(nr_to_plot))
        fig, ax = plt.subplots(nr_of_rows, nr_of_rows, sharex='col', sharey='row', figsize=(16, 8))
        fig.suptitle(f'Plot of nearest neighbors (NN) in layer {NN["layer name"]} with {confirmation_perc_NN}% of NN confirm with prediction')

        # plot input image and all nearest neighbors
        nr_NN_plotted = 0
        for i in range(nr_of_rows):
            for j in range(nr_of_rows):

                # format subplot
                ax[i, j].set_xticklabels([])
                ax[i, j].set_yticklabels([])

                if nr_NN_plotted + 1 >= nr_to_plot:
                    continue  # all intended images plotted

                if i + j == 0:
                    # plot input image
                    cax = ax[0, 0].imshow(render.vec2im(self.X_input), vmin=0, vmax=1)
                    # ax[0, 0].matshow(render.vec2im(self.X_input))
                    ax[0, 0].set_title(f'Input image; label {self.Y_input}; predict {self.Y_input_predict.round(2)}',
                                       fontsize=8)
                    continue

                ax[i, j].imshow(render.vec2im(NN['X'][nr_NN_plotted]), vmin=0, vmax=1)
                # ax[i, j].matshow(render.vec2im(NN['X'][nr_NN_plotted]))
                ax[i, j].set_title(f'NN {nr_NN_plotted}; label = {NN["Y"][nr_NN_plotted]}; distance = {round(NN["distances"][nr_NN_plotted], 4)}',
                                   fontsize=8)
                nr_NN_plotted += 1

        # finalize figure
        fig.subplots_adjust(right=0.8)
        # put colorbar at desire position
        cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        fig.colorbar(cax, cax=cbar_ax)
        # fig.tight_layout(rect=[0, 0, 0.95, .95])