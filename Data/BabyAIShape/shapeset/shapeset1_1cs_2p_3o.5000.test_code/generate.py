
from sample import *
from shapedefs import *


#==========================================================
class Generator(Sampler):
    
    def generate(self):
        pass


#==========================================================
class ShapeGenerator(Generator):
    __samplers__ = {'type': None,
                    'x': 0,
                    'y': 0,
                    'color': (0,0,0),
                    'texture': None,
                    'angle': 0}

    def __init__(self, registry, samplers):
        Sampler.__init__(self, None)
        
        self.registry = registry
        self.samplers = self.__class__.__samplers__.copy()
        self.samplers.update(samplers)
        for (k, sampler) in self.samplers.items():
            self.samplers[k] = samplerize(sampler)

    def generate(self):
        d = {}
        for (k, sampler) in self.samplers.items():
            d[k] = sampler.generate()
        return self.registry.create(**d)

    def can_produce(self, value):
        """
        The result of this generator is meant to be modified,
        except for its type.
        """
        if isinstance(value, str):
            return self.samplers['type'].can_produce(value)
        else:
            return hasattr(value, 'type') and self.samplers['type'].can_produce(value.type)


#==========================================================
class SceneGenerator(Generator):
    """
    This generator generates simple scenes under the following assumptions:
    - The color, shape and/or area of a shape can depend on the others.
      For instance, we do not want the background to be the same color
      as some shape.
    - Color, shape and area are however independent of each other.
    """

    def __init__(self, registry, nshapes, color_gen, texture_gen, shape_gen, area_gen, elong_gen, positioner = None, rng = None):
        """
        The arguments must respect the following constraints:
        
        len(color_gen) = len(texture_gen) = nshapes + 1
        len(type_gen) = len(area_gen) = len(elong_gen) = nshapes

        The last element of color_gen and texture_gen give the color and
        the texture of the background. Except for that, the ith return value
        of each generator controls the corresponding attribute of the ith shape.

        The positioner argument is a function which takes the scene and a list
        of all shapes generated and returns a bounding box for each. See
        SceneGenerator.positioner for information about the default.
        """
        Sampler.__init__(self, rng)
        
        self.registry = registry
        self.__badpos__ = 0
        self.__failures__ = 0

        self.nshapes = nshapes
        self.color_gen = color_gen
        self.texture_gen = texture_gen
        self.shape_gen = shape_gen
        self.area_gen = area_gen or ConstantSampler(None)
        self.elong_gen = elong_gen or ConstantSampler(None)
        if positioner:
            self.positioner = positioner

    def sample_x(self, shape, dimx):
        return self.rng.random() * (1-dimx)

    def sample_y(self, shape, dimy):
        return self.rng.random() * (1-dimy)

    def sample_xy(self, shape, dimx, dimy):
        return (self.sample_x(shape, dimx), self.sample_y(shape, dimy))

    def positioner(self, shapes): ### works
        nshapes = len(shapes)
        dims = [shape.dim() for shape in shapes]

        for (dimx, dimy) in dims:
            if dimx > 0.9 or dimy > 0.9:
                return False

        bboxs = [shape.bounding_box() for shape in shapes]
        bpols = [shape.bounding_polygon() for shape in shapes]

        max_attempts = 5
        for i in range(max_attempts):
            attempt = [self.sample_xy(shape, dimx, dimy)
                       for shape, (dimx, dimy) in zip(shapes, dims)]

            bpols = [[(px + x - oldx, py + y - oldy) for (px, py) in points] for (points, (x,y), ((oldx, oldy), (_1, _2))) in zip(bpols, attempt, bboxs)]
            
            for shape, (x,y), ((oldx, oldy), (_1, _2)), i in zip(shapes, attempt, bboxs, xrange(nshapes)):
                dx = x - oldx
                dy = y - oldy
                bboxs[i] = ((x, y), (_1 + dx, _2 + dy))
                shape.update(x = shape.x - oldx + x,
                             y = shape.y - oldy + y)

            success = True

            for (i, bpol1, bbox1) in zip(xrange(1, len(bpols)+1), bpols, bboxs):
                for (bpol2, bbox2) in zip(bpols[i:], bboxs[i:]):
                    if overlap(bbox1, bbox2) and polygon_overlap(bpol1, bpol2):
                        success = False
                        break
                if not success:
                    break

            if success:
                break

            self.__badpos__ = self.__badpos__ + 1
            success = False

        if not success:
            self.__failures__ = self.__failures__ + 1

        return success


    def generate(self):

        colors = self.color_gen.generate()
        bgcolor, colors = colors[0], colors[1:]

        textures = self.texture_gen.generate()
        bgtexture, textures = textures[0], textures[1:]
        
        shapes = self.shape_gen.generate()

        for shape, color, texture in zip(shapes, colors, textures):
            shape.update(color = color,
                         texture = texture)

        success = False
        max_attempts = 5
        for i in range(max_attempts):
            areas = self.area_gen.generate()
            elongs = self.elong_gen.generate()
            for shape, area, elong in zip(shapes, areas, elongs):
                shape.update_using_area_and_elongation(area, elong)
            success = self.positioner(shapes)
            if success:
                break
            
        if not success:
            return self.generate()

        return self.registry.create(type = 'scene',
                                    shapes = shapes,
                                    color = bgcolor,
                                    texture = bgtexture)



