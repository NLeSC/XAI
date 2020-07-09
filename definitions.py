# -*- coding: utf-8 -*-
"""
Created on 6/28/2020

Author: Joost Berkhout (VU, email: j2.berkhout@vu.nl)

Description: To find the root directory of XAI withing any subfolder so that
the code can be used without having to specifying the root. Specifically,
anywhere in the project you can use (if root is in Python path):

from definitions import ROOT_DIR

to be able to refer to files/folders from the root.
"""

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
