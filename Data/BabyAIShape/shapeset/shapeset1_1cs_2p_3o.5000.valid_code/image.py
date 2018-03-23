
from shape import *
from shapedefs import *
from pygame import *


def surface_to_vector(surface, mode, format):
    vec_ = surfarray.pixels3d(surface)
    vec = 0
    if format == 'ascii':
        vec = []
        for column in vec_:
            for colors in column:
                if mode == 'rgb':
                    vec += [x / 255.0 for x in colors]
                elif mode == 'gray':
                    vec.append(sum(colors) / 255.0 / 3.0)
    elif format == 'bin':
        if mode == 'rgb':
            return vec_.tostring()
        elif mode == 'gray':
            return "".join([chr(int(sum(colors) / 3.0)) for colors in column for column in vec_])
    return vec


#==========================================================
class Imager:

    __palette__ = None
    __palette_transparent__ = 255
    __transparent__ = (1,2,3)

    @classmethod
    def make_surface(cls, width, height):
        if cls.__palette__:
            surf = Surface((width, height), 0, 8)
            if display.get_active():
                surf.set_palette(cls.__palette__)
            surf.fill(cls.__palette_transparent__)
            surf.set_colorkey(cls.__palette_transparent__)
        else:
            surf = Surface((width, height))
            surf.fill(cls.__transparent__)
            surf.set_colorkey(cls.__transparent__)
        return surf

    @classmethod
    def apply_over_texture(cls, surface, texture):
        if texture:
            (width, height) = surface.get_size()
            img = image.load(texture)
            surf = cls.make_surface(width, height)
            (iwidth, iheight) = img.get_size()
            for i in xrange(0,width,iwidth):
                for j in xrange(0,height,iheight):
                    surf.blit(img, Rect((i,j),(iwidth,iheight)), None)
            surface.set_colorkey(None)
            surf.blit(surface, (0,0))
            if cls.__palette__:
                surf.set_colorkey(cls.__palette_transparent__)
            else:
                surf.set_colorkey(cls.__transparent__)
            return surf
        else:
            return surface


    def surface(self, x_res, y_res):
        pass

    def matrix(self, x_res, y_res):
        surf = self.surface(x_res, y_res)
        if self.__palette__:
            return surfarray.pixels2d(surf)
        else:
            return surfarray.pixels3d(surf)


#==========================================================
class RectangleImager(Imager, Rectangle):

    def surface(self, x_res, y_res):
        if self.angle == 0:
            surf = self.make_surface(int(round(self.x_size * x_res)), int(round(self.y_size * y_res)))
            surf.fill(self.color)
            surf = self.apply_over_texture(surf, self.texture)
        elif self.angle == pi/2:
            surf = self.make_surface(int(round(self.y_size * y_res)), int(round(self.x_size * x_res)))
            surf.fill(self.color)
            surf = self.apply_over_texture(surf, self.texture)
        else:
            ((minx, miny), (maxx, maxy)) = self.bounding_box()
            w, h = int(round((maxx - minx) * x_res)) + 1, int(round((maxy - miny) * y_res)) + 1
            surf = self.make_surface(w, h)
            points = [(int(round((x-minx)*x_res)), int(round((y-miny)*y_res))) for x,y in self.points()]
            draw.polygon(surf, self.color, points)
            surf = self.apply_over_texture(surf, self.texture)
        return surf


#==========================================================
class EllipseImager(Imager, Ellipse):

    def surface(self, x_res, y_res):
        w, h = int(round(self.x_radius * x_res * 2)) + 1, int(round(self.y_radius * y_res * 2)) + 1
        surf = self.make_surface(w, h)
        draw.ellipse(surf, self.color, Rect((0,0), (w, h)), 0)
        
        # Note 1: the y axis increases downwards, so the rotation is clockwise with respect to the coordinate system
        
        # Note 2: transform.rotate enlarges the surface so if it was filled beforehand, it would fit whole in the new surface.
        # This means the rotated ellipse will not touch the boundary of the rotated surface unless the angle is 0 or pi/2,
        # so there will be a margin around it.
        # The bounding box of the ellipse is calculated in the same way (see the class Ellipse), therefore the blitting code
        # in SceneImager is correct. If the bounding box code is changed (to be tighter, etc), it will not be correct anymore.
        surf = transform.rotate(surf, int(self.angle / pi * -180))

        surf = self.apply_over_texture(surf, self.texture)
        return surf


#==========================================================
class TriangleImager(Imager, Triangle):

    def surface(self, x_res, y_res):
        ((minx, miny), (maxx, maxy)) = self.bounding_box()
        w, h = int(round((maxx - minx) * x_res)) + 1, int(round((maxy - miny) * y_res)) + 1
        surf = self.make_surface(w, h)
        points = [(int(round((x-minx)*x_res)), int(round((y-miny)*y_res))) for x,y in self.points()]
        draw.polygon(surf, self.color, points)
        surf = self.apply_over_texture(surf, self.texture)
        
        return surf


#==========================================================
class SceneImager(Imager, Scene):

    def surface(self, x_res, y_res):
        w, h = x_res, y_res
        surf = self.make_surface(w, h)
        surf.fill(self.color)
        surf = self.apply_over_texture(surf, self.texture)
        for shape in self.shapes:
            ((minx, miny), (maxx, maxy)) = shape.bounding_box()
            surf.blit(shape.surface(x_res, y_res),
                      (minx * x_res, miny * y_res))

        return surf

