# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 20:19:44 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: In this script the LRP can be studied in an interactive way using
sliders and buttons.
"""

#from tools import data_loader, model_io, render, data_analysis
from tools import model_io, render, data_analysis
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import numpy as np
import settings
#import math
import os



# load trained neural network (nn)
nnName = 'nn_Linear_1024_2_Rect_Linear_2_2_SoftMax_(batchsize_10_number_iterations_10000).txt'
nn = model_io.read(os.path.join(settings.modelPath, nnName))

# unique shape rotation of squares and triangles
uniqShapeRot = data_analysis.unique_shapes()
uniqShapeRotSq = uniqShapeRot['square']
uniqShapeRotTr = uniqShapeRot['triangle']
numbRotSq = len(uniqShapeRotSq)
numbRotTr = len(uniqShapeRotTr)

# init figure
fig, axes = plt.subplots(figsize=(15, 5))
plt.axis('off')

# set locations for sliders
axcolor = 'lightgoldenrodyellow'

# init of all ax locations
axOrigImage = plt.axes([0.4, 0.125, 0.25, 0.75])
axNnPred = plt.axes([0.7, 0.125, 0.25, 0.75])
axShapeColor = plt.axes([0.1, 0.775, 0.2, 0.1], facecolor=axcolor)
axBackgroundColor = plt.axes([0.1, 0.575, 0.2, 0.1], facecolor=axcolor)
axShape = plt.axes([0.05, 0.275, 0.1, 0.2], facecolor=axcolor)
axSwitchColor = plt.axes([0.25, 0.375, 0.1, 0.1], facecolor=axcolor)
axRotateLeft = plt.axes([0.05, 0.12, 0.1, 0.1], facecolor=axcolor)
axRotateRight = plt.axes([0.25, 0.12, 0.1, 0.1], facecolor=axcolor)
axColormapLRP = fig.add_axes([0.95, 0.125, 0.01, 0.75])

# set sliders
sShapeColor = Slider(axShapeColor, 'Shape color', 0, 1, valinit=.4)
sBackgroundColor = Slider(axBackgroundColor, 'Background color', 0, 1, valinit=.5)
bRotateLeft = Button(axRotateLeft, 'Rotate shape left')
bRotateRight = Button(axRotateRight, 'Rotate shape right')
rbShape = RadioButtons(axShape, ('square', 'triangle'), active=0)
bSwitchColor = Button(axSwitchColor, 'Switch color')


def plot_shape_and_lrp(val):
    global rotateIdx, shape, nn, method
    shapeColor = sShapeColor.val
    backgroundColor = sBackgroundColor.val
    typeMethod = method

    im = np.array(uniqShapeRot[shape][rotateIdx])
    im[im == 1] = shapeColor
    im[im == 0] = backgroundColor

    info = 'shape color = {}, background color = {}, rotateIdx = {}, shape = {}.'.format(shapeColor, backgroundColor, rotateIdx, shape)
    fig.suptitle(info)
    axOrigImage.imshow(render.vec2im(im), cmap='gray_r', vmin=0, vmax=1)

    nnPred = nn.forward(np.array([im]))
    #lrpScores = nn.lrp(nnPred, 'alphabeta', 2)
    lrpScores = nn.lrp(nnPred, typeMethod, 2)
    if np.isnan(np.sum(lrpScores[0])):
        print('Warning: NaN values. Most likely because score after first layer'
              ' gives two negative numbers and you get division by 0.')
    caxNnPred = axNnPred.imshow(render.vec2im(lrpScores[0]), cmap='jet')
    fig.colorbar(caxNnPred, cax=axColormapLRP)
    infoNNPred = 'NN probabilities: square = {}, triangle = {}'.format(round(nnPred[0][0], 2), round(nnPred[0][1], 2))
    axNnPred.set_title(infoNNPred)
    fig.canvas.draw()
    fig.canvas.draw_idle()
    print('Done (re)drawing figure.')


rotateIdx = 0
def rotate_update_left(val):
    global rotateIdx
    rotateIdx -= 1
    plot_shape_and_lrp(val)


def rotate_update_right(val):
    global rotateIdx
    rotateIdx += 1
    plot_shape_and_lrp(val)


shape = 'square'
method = 'alphabeta'
def shape_update(shape_label):
    global shape
    shape = shape_label
    plot_shape_and_lrp(shape_label)


def switch_colors(val):
    oldShapeColor, oldBackgroundColor = sBackgroundColor.val, sShapeColor.val
    sShapeColor.set_val(oldShapeColor)
    sBackgroundColor.set_val(oldBackgroundColor)
    plot_shape_and_lrp(val)


shape_update(shape)
sShapeColor.on_changed(plot_shape_and_lrp)
sBackgroundColor.on_changed(plot_shape_and_lrp)
bRotateLeft.on_clicked(rotate_update_left)
bRotateRight.on_clicked(rotate_update_right)
rbShape.on_clicked(shape_update)
bSwitchColor.on_clicked(switch_colors)

plt.show()
