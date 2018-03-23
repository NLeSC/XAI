
import numpy
from random import Random
from math import *
from utils import *
import sys
import re
from os.path import exists

class ImageMaker:
    def __init__(self, parms):
        self.parms = parms
        a = numpy.uint8([])
        a.resize(parms.xres, parms.yres)
        self.array = a
        self.rng = Random()
        self.rng.seed(parms.seed)
        
    def make_image(self, text = None):
        parms = self.parms
        
        color1 = self.rng.randint(0, parms.colrange - 1)
        if color1 <= parms.sep:
            color2 = self.rng.randint(color1 + parms.sep + 1, parms.colrange - 1)
        elif color1 >= parms.colrange - parms.sep - 1:
            color2 = self.rng.randint(0, color1 - parms.sep - 1)
        else:
            color2 = (color1 + self.rng.randint(parms.sep, parms.colrange - parms.sep - 1)) % parms.colrange
        angle = self.rng.randint(0, parms.ares) / float(parms.ares + 1) * pi
        ax = sin(angle)
        ay = cos(angle)
        

        if self.rng.random() < parms.smoothpct:
            b = 5 * parms.xres
        else:
            b = self.rng.randint(*parms.brange)

        cx = parms.xres / 2.0
        cy = parms.yres / 2.0
        for i in xrange(parms.xres):
            for j in xrange(parms.yres):
                x = i - cx
                y = j - cy
                if x*ax + y*ay + b > 0:
                    self.array[i][j] = color1
                else:
                    self.array[i][j] = color2
        self.color1 = color1
        self.color2 = color2
        self.ax = ax
        self.ay = ay
        self.angle = angle
        self.b = b
        return self.array # copy the return value if you need to keep it

    def tostring(self):
        s = ""
        parms = self.parms
        for i in xrange(parms.yres):
            for j in xrange(parms.xres):
                if self.array[j][i] == self.color1:
                    s += "."
                else:
                    s += "X"
            s += "\n"
        return s

    def header(self):
        parms = self.parms
        ares = parms.ares * 2 + 1
        bres = parms.brange[1] - parms.brange[0] + 1
        abits = int(ceil(log(ares) / log(2)))
        bbits = int(ceil(log(bres) / log(2)))
        return "i:%d:%d:%d i:1:%d:%d i:1:%d:%d\n" % (parms.xres * parms.yres, parms.colrange - 1, int(ceil(log(parms.colrange) / log(2))),
                                                     ares - 1, abits,
                                                     bres - 1, bbits)

    def tocmatline(self):
        parms = self.parms
        nbits = int(ceil(log(parms.colrange) / log(2)))
        img = self.array.copy()
        img.resize((parms.xres * parms.yres, ))
        if nbits == 2:
            img_compressed = compress_array_2bits(img)
        else:
            img_compressed = compress_array(img, nbits)
        return (img_compressed.tostring()
                + chr(int(self.angle / pi * (parms.ares + 1)))
                + chr(self.b - parms.brange[0]))

class FrozenD:
    def __init__(self, *dicts, **dict2):
        for dict in dicts:
            self.__dict__.update(dict)
        self.__dict__.update(dict2)
    def __setattr__(self, attr, value):
        self.__dict__.setdefault(attr, value)

def parseval(value):
    if value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False
    elif value[0] == '[' or value[0] == '{' or value[0] == '(' or value[0] == '"' or value[0] == "'":
        return eval(value)
    try:
        val = value
        val = float(value)
        val = int(value) # int("1.0") fails
        return val
    except Exception:
        return val

def dotask(parms):
    parms.task = "view"
    parms.n = 10

    im = ImageMaker(parms)

    if parms.task == "view":
        for i in xrange(parms.n):
            im.make_image()
            print im.tostring()
    elif parms.task == "view2":
        for i in xrange(parms.n):
            im.make_image()
            print im.array
    elif parms.task == "write":
        parms.tag = "train"
        parms.filename = ("EDGES_%d_%dx%d_%dcol_%dsep_%dprec_%doff_%dsmooth_%dseed.%s.cmat"
                          % (parms.n,
                             parms.xres, parms.yres,
                             parms.colrange, parms.sep,
                             parms.ares, parms.brange[1],
                             int(parms.smoothpct * 100),
                             parms.seed,
                             parms.tag))
        if exists(parms.filename):
            print "Warning: %s already exists." % parms.filename
            return
        f = open(parms.filename, "w")
        f.write("%d %s" % (parms.n, im.header()))
        for i in xrange(parms.n):
            im.make_image()
            f.write(im.tocmatline())


if __name__ == "__main__":

    args = [arg.split("=") for arg in sys.argv[1:]]
    args = [[option, parseval(value)] for option, value in args]
    
    parms = FrozenD()
    for option, value in args:
        if re.match("[a-zA-Z][a-zA-Z0-9_]*", option):
            setattr(parms, option, value)

    parms.seed = 1
    parms.xres = 5
    parms.yres = parms.xres
    parms.brange = [-1, 1]
    parms.colrange = 4
    parms.sep = 1
    parms.ares = 31
    parms.smoothpct = 0.5
    
    dotask(parms)

