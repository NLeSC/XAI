
from standard_dataset import *
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
    all_args['gram_dictionaries'] = d.problem.gram_dictionaries
    all_args['answer_words'] = d.problem.answer_words
    all_args['question_words'] = d.problem.question_words
    all_args['number_words_max'] = d.problem.number_words_max
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

""" % {'name': 'problem_convert',
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
    return StandardDataset(**d.__dict__)


def dataset_def(args_d):

    p = D()

    rng = Random()
    p.rng = rng
    
    # Minimal amount of objects
    p.object_min = 1

    # Maximal amount of objects (currently it should be the same as object_min, as a variable amount of shapes is not support)
    p.object_max = 1
    

    args = D(use_angles = True,                # True if the shapes can be rotated
             area_min = 0.01,                  # Minimal area of an object
             area_max = 0.40 / p.object_max)   # Maximal area of an object (scales down with the amount of shapes)

    for key, value in args_d.items():
        if hasattr(args, key):
            del args_d[key]
            setattr(args, key, value)
    

    # Names of the possible shapes
    p.shape_names = ['rectangle', 'ellipse', 'triangle']

    # Prior probabilities of the aforementioned shapes
    p.shape_probs = [1./len(p.shape_names) for i in xrange(len(p.shape_names))]


    if args.use_angles:
        angle_sampler = UniformSampler(0, 2*pi, rng)
    else:
        angle_sampler = 0

    # One sampler per shape type. The parameters that are put to 0 will be set using angle and elongation.
    p.shape_samplers = [{'type': 'rectangle', 'x_size': 0, 'y_size': 0, 'angle': angle_sampler},
                        {'type': 'ellipse', 'x_radius': 0, 'y_radius': 0, 'angle': angle_sampler},
                        {'type': 'triangle', 'baselength': 0, 'height': 0, 'peakoffset': UniformSampler(0,1,rng), 'angle': angle_sampler}]

#     # List of colors. The position of a color in that list is the integer index that will be associated to it.
#     p.palette = [[0,0,0], [255,0,0], [0,255,0], [0,0,255], [255,255,0], [255,0,255], [0,255,255], [255,255,255]]

#     # Names of the colors in the palette.
#     p.color_names = ['black', 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'white']

    # GRAYSCALE palette
    lg=0.73*255
    dg=0.43*255
    p.palette = [[0,0,0], [dg,dg,dg], [lg,lg,lg], [255,255,255]]
    p.color_names = ['black','dark gray','light gray','white']

    # If True, the objects in the scene will be updated using an area value and an elongation value.
    # else, they will keep the parameters set by p.shape_samplers.
    p.area_elong_update = True

    # Maximal elongation of an object (ratio between width and height, before rotation)
    elong_range = 5.0

    # This is a list of [probability, sampler, binary encoding, english] values.
    # Since we won't describe this attribute, we simply generate a random value.
    p.elong_value = [[1.0, LogSpaceSampler(1. / elong_range, elong_range, rng), [1, 0], 'NA']]


    area_min = args.area_min
    area_max = args.area_max
    # Margin between a big object and a small object
    area_margin = (area_max - area_min) / 2
    area_bandwidth = (area_max - area_min - area_margin) / 2
    area_thresholds = [area_min, area_min + area_bandwidth, area_max - area_bandwidth, area_max]
    area_bands = zip(area_thresholds[:-1], area_thresholds[1:])
    # Names given to objects that fall in the area ranges
    area_names = ['small', 'NA', 'large']
    total = area_max - area_min
    total_bandwidth = area_max - area_min - area_margin
    area_probs = [(band[1] - band[0]) / total for band in area_bands]
    p.area_value = [[prob, UniformSampler(band[0], band[1], rng), None, name] for (prob, band, name) in zip(area_probs, area_bands, area_names)]
    
    # Margin between the zone where objects are said to be to the left of the screen
    # and the zone where they are said to be to the right of the screen.
    x_margin = y_margin = 0.3

    Interval = lambda min,max: UniformSampler(min, max, rng) # This allows for a clearer notation in what follows

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

    ################################################
#    p.dict_seed = 1
#    p.gram_dictionaries = 
#    p.answer_words = 
#    p.question_words = 
#    p.number_words_max = 
    ################################################

    p.language_question = {'color': 1, 'shape': 1, 'location_hor': 1, 'location_vert': 1, 'size': 1}
    p.language_sentence = 'one'
    if p.object_max == 1:
        p.language_objects = 1
    else:
        p.language_objects = 2
    p.language_form = 'question/answer'
    p.language_background = 0
    p.language_negation = 'none'


    ################################################
    d = D()
    # Amount of examples to generate
    d.n_examples = 1000

    # Amount of examples to use to generate the dictionary
    d.dict_n_examples = 1000

    # Data folder to put files in
    d.data_directory = '/cluster/opter/data/babyAI/textual_v2/'

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

    # Prefix of the files
    d.tag = 'BABYAI_gray_' + str(d.n_examples) + 'x' + str(p.object_max) + 'obj_'  + str(p.x_res) + 'x' + str(p.y_res) + '.color-size-location-shape.' + d.tag


    return p, d, args

