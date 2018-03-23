
from shape import *
from math import *
from utils import *


#==========================================================
class BaseShape(Shape):
    
    __attributes__ = [('x', 0), ('y', 0), 'color', ('texture', None), ('angle', 'not yet implemented')]
    
    def elongation(self):
        """
        Ratio between one side and the other, typically x_size / y_size before a rotation is applied.
        """
        pass

    def bounding_box(self):
        return bpol_to_bbox(self.bounding_polygon())

    def update_using_area_and_elongation(self, area, elongation):
        pass

    def update_using_bbox_min(self, new_minx, new_miny):
        ((minx, miny), (maxx, maxy)) = self.bounding_box()
        self.update(x = new_minx + (maxx-minx)/2,
                    y = new_miny + (maxy-miny)/2)

    def centroid(self):
        return (self.x, self.y)

    def scale(self, scale):
        pass


#==========================================================
class Rectangle(BaseShape):
    
    __attributes__ = ['x_size', 'y_size']

    def bounding_polygon(self):
        return self.points()

    def rawpoints(self):
        x,y,dw,dh = self.x, self.y, self.x_size/2, self.y_size/2
        return [(x-dw, y-dh), (x-dw, y+dh), (x+dw, y+dh), (x+dw, y-dh)]

    def points(self):
        return rotate_polygon(self.rawpoints(), self.angle, (self.x, self.y))

    def area(self):
        return self.x_size * self.y_size

    def elongation(self):
        return float(self.x_size) / self.y_size

    def update_using_area_and_elongation(self, area, elongation):
        y_size = sqrt(area / elongation)
        x_size = area / y_size
        self.update(x_size = x_size,
                    y_size = y_size)

    def scale(self, scale):
        self.update(x_size = self.x_size * scale,
                    y_size = self.y_size * scale)


#==========================================================
class Square(Rectangle):
    __ratio__ = 1.20
    def update_using_area_and_elongation(self, area, elongation):
        elongation = exp(tanh(log(elongation)) * log(self.__ratio__))
        y_size = sqrt(area / elongation)
        x_size = area / y_size
        self.update(x_size = x_size,
                    y_size = y_size)
    

#==========================================================
class Ellipse(BaseShape):

    
    __attributes__ = ['x_radius', 'y_radius']

    # Note: the bounding box of the ellipse should be calculated using bpol_to_bbox on
    # this particular bounding polygon because of how Ellipse is currently drawn by
    # EllipseImager. If this method is changed to become tighter, override bounding_box
    # using the code below (or change EllipseImager).
    def bounding_polygon(self):
        x,y,dw,dh = self.x, self.y, self.x_radius, self.y_radius
        return rotate_polygon([(x-dw, y-dh), (x-dw, y+dh), (x+dw, y+dh), (x+dw, y-dh)], self.angle, (self.x, self.y))

    def area(self):
        return pi * self.x_radius * self.y_radius

    def elongation(self):
        return float(self.x_radius) / self.y_radius

    def update_using_area_and_elongation(self, area, elongation):
        y_radius = sqrt(area / elongation / pi)
        x_radius = area / pi / y_radius
        self.update(x_radius = x_radius,
                    y_radius = y_radius)
        
    def scale(self, scale):
        self.update(x_radius = self.x_radius * scale,
                    y_radius = self.y_radius * scale)


#==========================================================
class Circle(Ellipse):
    __ratio__ = 1.20
    def update_using_area_and_elongation(self, area, elongation):
        elongation = exp(tanh(log(elongation)) * log(self.__ratio__))
        y_radius = sqrt(area / elongation / pi)
        x_radius = area / pi / y_radius
        self.update(x_radius = x_radius,
                    y_radius = y_radius)



#==========================================================
class Triangle(BaseShape):
    """
    This class represents a triangle. The triangle is defined as a base triangle
    with a side resting on the x-axis and then rotated by 'angle' degrees.

    It contains several important attributes:
    - baselength: length of the side resting on the x axis
    - height: height of the triangle - the area is baselength * height / 2
    - peakoffset: real between 0 and 1 indicating where the peak is located above the base

    The three points of the triangle, before rotation, are:
    (0, 0), (self.baselength, 0) and (self.peakoffset * self.baselength, self.height)
    """
    
    __attributes__ = ['baselength', 'height', 'peakoffset']

    def bounding_polygon(self):
        return self.points()

    def area(self):
        return self.baselength * self.height / 2.0

    def elongation(self):
        return float(self.baselength) / self.height

    def update_using_area_and_elongation(self, area, elongation):
        height = sqrt(2 * area / elongation)
        baselength = 2 * area / height
        self.update(height = height,
                    baselength = baselength)

    def rawpoints(self):
        return [(0., 0.), (self.peakoffset * self.baselength, self.height), (self.baselength, 0.)]
    
    def points(self):
        """
        Returns the three points defining the triangle (after rotation of 'angle' degrees)
        """
        rawpoints = self.rawpoints()
        (offx, offy) = pminus(self.centroid(), pavg(rawpoints))
        return rotate_polygon([(x + offx, y + offy) for (x,y) in rawpoints], self.angle, (self.x, self.y))

    def scale(self, scale):
        self.update(baselength = self.baselength * scale,
                    height = self.height * scale)


#==========================================================
class Scene(Shape):
    """
    This class represents a Scene containing several shapes. Here are its attributes:
    - color: the background color of the scene
    - texture: the background texture of the scene
    - shapes: a list of shapes on the scene
    The scene is a 1x1 square
    """

    __attributes__ = ['color', ('texture', None), 'shapes', ('text', None)]

    def area(self):
        return 1

    def bounding_box(self):
        return ((0,0), (1,1))
