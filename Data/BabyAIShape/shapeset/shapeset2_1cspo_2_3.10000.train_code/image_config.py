
from image_dataset import *
from standard_problem import *
from sample import *
from image import *
from random import *
import os

def write_dataset(all_args):
    d = dataset(**all_args)
    p = d.problem
    dir = os.path.join(d.data_directory, d.tag + "_code")
    if os.system("mkdir %s" % dir):
        raise "Dataset already exists: " + dir
    os.system("cp *.py %s" % dir)

    file_contents = """
    
import sys
import os

sys.path.append('%(tag)s_code')

from %(name)s import *

d = dataset(%(args)s)
d.data_directory = "."

try:
    task = sys.argv[1]
    args = sys.argv[2:]

    fn = getattr(d, task)
    
except Exception, e:
    print 'Usage: %%(prog)s write_formats [format]*\\n       %%(prog)s view' %% {'prog': sys.argv[0]}
    sys.exit()

fn(*args)

""" % {'name': 'image_config',
       'args': ",".join([key + "=" + repr(value) for key, value in all_args.items()]),
       'tag': d.tag}

    script = os.path.join(d.data_directory, d.tag + ".py")
    f = open(script, "w")
    f.write(file_contents)
    f.close()

    os.system("chmod ugo-w %s %s" % (os.path.join(dir, '*.py'), ""))


def dataset(**args):
    p, d, args = dataset_def(args)
    d.problem = StandardProblem(**p.__dict__)
    return ImageDataset(**d.__dict__)


def dataset_def(args_d):

    p = D()

    rng = Random()
    p.rng = rng
    
    # Minimal amount of objects
    p.object_min = 1

    # Maximal amount of objects (currently it should be the same as object_min, as a variable amount of shapes is not support)
    p.object_max = 1
    
    args = D(shapeset = 1,
             free = "",
             constrained = "",
             fixed = "")

    for key, value in args_d.items():
        if hasattr(args, key):
            del args_d[key]
            setattr(args, key, value)

    args.free = args.free.split(",")
    args.constrained = args.constrained.split(",")
    args.fixed = args.fixed.split(",")
    

    # Names of the possible shapes
    p.shape_names = ['rectangle', 'ellipse', 'triangle']

    # Prior probabilities of the aforementioned shapes
    p.shape_probs = [1./len(p.shape_names) for i in xrange(len(p.shape_names))]

    if 'orientation' in args.free:
        rect_angle = UniformSampler(0, pi / 2, rng)
        ell_angle = UniformSampler(0, pi / 2, rng)
        tri_angle = UniformSampler(0, 2 * pi, rng)
    elif 'orientation' in args.constrained:
        rect_angle = UniformSampler(0, 0.1, rng)
        ell_angle = UniformSampler(0, 0.1, rng)
        tri_angle = UniformSampler(0, 0.1, rng)
    elif 'orientation' in args.fixed:
        rect_angle = 0
        ell_angle = 0
        tri_angle = 0

    if args.shapeset == 1:
        tri_peak = 0.5
    else:
        tri_peak = UniformSampler(0,1,rng)
        

    # One sampler per shape type. The parameters that are put to 0 will be set using angle and elongation.
    p.shape_samplers = [{'type': 'rectangle', 'x_size': 0, 'y_size': 0, 'angle': rect_angle},
                        {'type': 'ellipse', 'x_radius': 0, 'y_radius': 0, 'angle': ell_angle},
                        {'type': 'triangle', 'baselength': 0, 'height': 0, 'peakoffset': tri_peak, 'angle': tri_angle}]

    # List of colors. The position of a color in that list is the integer index that will be associated to it.
    p.palette = [[0,0,0], [255,0,0], [0,255,0], [0,0,255], [255,255,0], [255,0,255], [0,255,255], [255,255,255]]

    # Names of the colors in the palette.
    p.color_names = ['black', 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'white']

    # If True, the objects in the scene will be updated using an area value and an elongation value.
    # else, they will keep the parameters set by p.shape_samplers.
    p.area_elong_update = True


    if args.shapeset == 1:
        p.elong_value = [[1.0, ConstantSampler(1.0), [1, 0], 'NA']]
    else:
        # Maximal elongation of an object (ratio between width and height, before rotation)
        elong_range = 3.0
        p.elong_value = [[1.0, LogSpaceSampler(1. / elong_range, elong_range, rng), [1, 0], 'NA']]


    if 'size' in args.free:
        p.area_value = [[1.0, UniformSampler(0.1, 0.4, rng)]]
    elif 'size' in args.constrained:
        p.area_value = [[1.0, UniformSampler(0.15, 0.25, rng)]]
    elif 'size' in args.fixed:
        p.area_value = [[1.0, ConstantSampler(0.2)]]


#     if 'position' in args.free:
#         x_sampler = UniformSampler(0.0, 1.0)
#         y_sampler = UniformSampler(0.0, 1.0)
#     elif 'position' in args.constrained:
#         x_sampler = UniformSampler(0.45, 0.55)
#         y_sampler = UniformSampler(0.45, 0.55)
#     elif 'position' in args.fixed:
#         x_sampler = ConstantSampler(0.5)
#         y_sampler = ConstantSampler(0.5)
        

    class MySceneGenerator(SceneGenerator):

        def sample_xy(self, shape, dimx, dimy):
            if 'position' in args.free:
                return SceneGenerator.sample_xy(self, shape, dimx, dimy)
            elif 'position' in args.constrained:
                return (0.45 + 0.1 * rng.random() - dimx / 2,
                        0.45 + 0.1 * rng.random() - dimy / 2)
            elif 'position' in args.fixed:
                return (0.5 - dimx / 2, 0.5 - dimy / 2)

    p.scene_generator = MySceneGenerator
    
    # Margin between the zone where objects are said to be to the left of the screen
    # and the zone where they are said to be to the right of the screen.
    x_margin = y_margin = 0.3

    Interval = lambda min,max: UniformSampler(min, max, rng) # This allows for a clearer notation in what follows


    # useless ############################################################
    
    # Intervals corresponding to the left, middle (NA) and right zones
    p.x_value = [[Interval(0.0, 0.5 - x_margin/2.0), None, 'left'],
                 [Interval(0.5 - x_margin/2.0, 0.5 + x_margin/2.0), None, 'NA'],
                 [Interval(0.5 + x_margin/2.0, 1.0), None, 'right']]
    
    # Intervals corresponding to the top, middle (NA) and bottom zones
    p.y_value = [[Interval(0.0, 0.5 - y_margin/2.0), None, 'top'],
                 [Interval(0.5 - y_margin/2.0, 0.5 + y_margin/2.0), None, 'NA'],
                 [Interval(0.5 + y_margin/2.0, 1.0), None, 'bottom']]


    # Margin for which we do not compare the positions of the objects
    # If the relative position is between -margin/2 and margin/2 we don't compare.
    xcmp_margin = ycmp_margin = 0.36

    # Intervals for comparing the x coordinate
    p.xcmp_value = [[Interval(-1.0, - xcmp_margin/2.0), None, 'right'],
                    [Interval(- xcmp_margin/2.0, xcmp_margin/2.0), None, 'NA'],
                    [Interval(xcmp_margin/2.0, 1.0), None, 'left']]

    # Intervals for comparing the y coordinate
    p.ycmp_value = [[Interval(-1.0, - ycmp_margin/2.0), None, 'lower'],
                    [Interval(- ycmp_margin/2.0, ycmp_margin/2.0), None, 'NA'],
                    [Interval(ycmp_margin/2.0, 1.0), None, 'higher']]


    inf = float('inf') # or = 1e300000
    
    # Margin to compare the area. If the ratio of areas is between margin and 1/margin,
    # we do not compare them.
    areacmp_margin = 0.5
    # nb: the third sampler (with inf) can't actually generate anything
    p.areacmp_value = [[Interval(0, 1 - areacmp_margin), None, 'bigger'],
                       [Interval(1 - areacmp_margin, 1. / (1 - areacmp_margin)), None, 'NA'],
                       [Interval(1. / (1 - areacmp_margin), inf), None, 'smaller']]
    ######################################################################


    # Registry used to build the scenes.
    p.registry = Registry(__base__ = Imager,
                          rectangle = RectangleImager,
                          ellipse = EllipseImager,
                          triangle = TriangleImager,
                          scene = SceneImager)
    
    # x and y resolutions of the images (for training)
    p.x_res = 32
    p.y_res = 32

    # x and y resolutions of the images (for viewing)
    p.x_res_view = 200
    p.y_res_view = 200


    p.language_question = {'color': 1, 'shape': 1, 'location_hor': 1, 'location_vert': 1, 'size': 1}
    p.language_sentence = 'one'
    p.language_objects = 2
    p.language_form = 'question/answer'
    p.language_background = 0
    p.language_negation = 'none'


    ################################################
    d = D()
    # Amount of examples to generate
    d.n_examples = 5000

    # Data folder to put files in
    d.data_directory = '/cluster/pauli/data/babyAI/curriculum/'

    # Extension of the files that contain the complete, symbolic descriptions of the scenes.
    d.raw_ext = 'raw'
    # Extension of the files that contain the image data (one vector per line)
    d.img_ext = 'img'
    # Format of the image. Can be either 'palette' for one value per pixel or 'rgb' for 3 values per pixel
    d.img_format = 'palette'
    # Format of the file that contains the textual descriptions of the images.
    d.desc_ext = 'desc'
    
    # True if we want to compress the data
    d.compress = True

    # seed to start the sequence
    d.seed = random()

    if not args_d.has_key('seed'):
        print "Warning: no seed specified for this dataset. Picking a random seed."


    ################################################
    p.__dict__.update(args_d)
    d.__dict__.update(args_d)


    d.tag = 'shapeset%s_1%s_2%s_3%s.%s.%s' % (args.shapeset,
                                              "".join([x[0] for x in args.free if x]),
                                              "".join([x[0] for x in args.constrained if x]),
                                              "".join([x[0] for x in args.fixed if x]),
                                              d.n_examples,
                                              d.tag)

    return p, d, args

