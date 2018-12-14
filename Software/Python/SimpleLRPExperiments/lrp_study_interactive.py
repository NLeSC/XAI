# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 20:19:44 2018

Author: Joost Berkhout (CWI, email: j.berkhout@cwi.nl)

Description: In this script the LRP can be studied in an interactive way using
sliders and buttons.
"""

from tools import data_loader, model_io, render, data_analysis
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import numpy as np
import settings
import math


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
sShapeColor = Slider(axShapeColor, 'Shape color', 0, 1, valinit=.4, valstep=.01)
sBackgroundColor = Slider(axBackgroundColor, 'Background color', 0, 1, valinit=.5, valstep=.01)
sRotateLeft = Button(axRotateLeft, 'Rotate shape left')
sRotateRight = Button(axRotateRight, 'Rotate shape right')
sShape = RadioButtons(axShape, ('square', 'triangle'), active=0)
sSwitchColor = Button(axSwitchColor, 'Switch color')


def plot_shape_and_lrp(val):
    global rotateIdx, shape, nn
    shapeColor = sShapeColor.val
    backgroundColor = sBackgroundColor.val

    im = np.array(uniqShapeRot[shape][rotateIdx])
    im[im == 1] = shapeColor
    im[im == 0] = backgroundColor

    info = 'shape color = {}, background color = {}, rotateIdx = {}, shape = {}.'.format(shapeColor, backgroundColor, rotateIdx, shape)
    fig.suptitle(info)
    axOrigImage.imshow(render.vec2im(im), cmap='gray_r', vmin=0, vmax=1)

    nnPred = nn.forward(np.array([im]))
    lrpScores = nn.lrp(nnPred, 'alphabeta', 2)
    caxNnPred = axNnPred.imshow(render.vec2im(lrpScores[0]), cmap='jet')
    fig.colorbar(caxNnPred, cax=axColormapLRP, shrink=0.0001)
    infoNNPred = 'NN probabilities: square = {}, triangle = {}'.format(round(nnPred[0][0], 2), round(nnPred[0][1], 2))
    axNnPred.set_title(infoNNPred)
    fig.canvas.draw_idle()


rotateIdx = 0
def rotate_update_left(val):
    global rotateIdx, shape
    rotateIdx -= 1
    if shape == 'square':
        rotateIdx = rotateIdx % numbRotSq
    else:
        rotateIdx = rotateIdx % numbRotTr
    plot_shape_and_lrp(val)


def rotate_update_right(val):
    global rotateIdx, shape
    rotateIdx += 1
    if shape == 'square':
        rotateIdx = rotateIdx % numbRotSq
    else:
        rotateIdx = rotateIdx % numbRotTr
    plot_shape_and_lrp(val)


shape = 'square'
def shape_update(label):
    global rotateIdx, shape
    shape = label
    print(label)
    if shape == 'square':
        rotateIdx = rotateIdx % numbRotSq
    else:
        rotateIdx = rotateIdx % numbRotTr
    plot_shape_and_lrp(label)


def switch_colors(val):
    sShapeColor.val, sBackgroundColor.val = sBackgroundColor.val, sShapeColor.val
    sShapeColor.set_val(sShapeColor.val)
    sBackgroundColor.set_val(sBackgroundColor.val)
    plot_shape_and_lrp(val)


sShapeColor.on_changed(plot_shape_and_lrp)
sBackgroundColor.on_changed(plot_shape_and_lrp)
sRotateLeft.on_clicked(rotate_update_left)
sRotateRight.on_clicked(rotate_update_right)
sShape.on_clicked(shape_update)
sSwitchColor.on_clicked(switch_colors)

plt.show()
