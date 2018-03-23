
from utils import *
from registry import *


class Shape(Registered):
    """
    This is the base class for a shape. New shapes should subclass Shape or
    another shape which does.
    """

    """
    The registry maps shape names to the class they correspond to.
    Use ShapeSubclass.register(name) to fill it.
    """
    __registry__ = {}


    """
    Defines the default value of __check_validity__ for shape instances.
    """
    __check_validity_default__ = False


    __attributes__ = []


    def bounding_box(self):
        """
        Returns a bounding box in which the shape is contained. The bounding
        box is of the form ((minx, miny), (maxx, maxy)).
        """
        pass

    def bounding_polygon(self):
        """
        Returns a bounding polygon in which the shape is contained. Should be
        at least as tight as the bounding box.
        """
        return self.bounding_box()

    def dim(self):
        """
        Dimensions (width, height) of the bounding box.
        """
        ((minx, miny), (maxx, maxy)) = self.bounding_box()
        return (maxx - minx, maxy - miny)

    def centroid(self):
        """
        Center of mass of the shape
        """
        pass
    
    def area(self):
        """
        Returns the true area of the shape.
        """
        pass

