
from dataset import *
from registry import *
from pygame import *
from utils import *
import image
import sys
import os
import re

# import grammar_v5 as grammar
# import text_encode as encode
# encode.globals_init()

class SceneIterator:

    def __init__(self, n, gen, seed):
        gen.set_seed(seed)
        self.gen = gen
        self.n = n

    def __iter__(self):
        return self

    def next(self):
        if self.n:
            self.n = self.n - 1
            scene = self.gen.generate()
            return scene
        else:
            raise StopIteration()



class ConstrainedSceneIterator:

    def __init__(self, n, gen, seed, constraint):
        gen.set_seed(seed)
        grammar.reseed_grammar(seed)
        self.gen = gen
        self.n = n
        self.constraint = constraint

    def __iter__(self):
        return self

    def next(self):
        if self.n:
            scene = self.gen.generate()
            while not self.constraint(scene):
                scene = self.gen.generate()
            self.n = self.n - 1
            return scene
        else:
            raise StopIteration()

    


        
class SceneIteratorWrapper(SceneIterator):

    def __init__(self, n, gen, seed, f):
        SceneIterator.__init__(self, n, gen, seed)
        self.f = f

    def next(self):
        return self.f(SceneIterator.next(self))
    


class ImageDataset(Dataset):

    __attributes__ = ['problem',
                      ('raw_ext', 'raw'),
                      ('img_ext', 'img'),
                      ('img_format', 'rgb'),
                      ('desc_ext', 'desc'),
                      ('text_ext', 'txt'),
                      ('amat_ext', 'amat'),
                      ('svm_ext', 'libsvm'),
                      ('cmat_ext', 'cmat'),
                      ('compress', True),
                      ('orientation_granularity', 256),
                      ('size_granularity', 256),
                      ('xpos_granularity', 256),
                      ('ypos_granularity', 256),
                      ('elongation_granularity', 256),
                      ('elongation_sat', 2.0)]

    def __init__(self, **args):
        Dataset.__init__(self, **args)

    def stream(self, n_examples = None):
        
        if not n_examples:
            n_examples = self.n_examples
            
        return SceneIterator(n_examples, self.problem, self.seed)
        
    def list_formats(self):
        formats = []
        for member in dir(self):
            if member.startswith('format_') and not member.endswith('header'):
                formats.append(member[7:len(member)])
        return formats

    def write_formats(self, *formats):
        if not formats:
            return
        elif isinstance(formats[0], int):
            n_examples = formats[0]
            formats = formats[1:]
        else:
            n_examples = self.n_examples
        
        supported_formats = self.list_formats()
        [raise_("Error in write_formats - unsupported format: " + format) for format in formats if not format in supported_formats]
        
        formats_files = zip(['format_' + format for format in formats],
                            [self.open(getattr(self, format + "_ext"), 'wb') for format in formats])
        for format, file in formats_files:
            s = getattr(self, format + "_header")()
            if s is None:
                print "Rejected example."
            else:
                file.write(s)
        report = n_examples / 100
        i = 0
        for scene in self.stream(n_examples):
            i += 1 # we don't want a dot right now
            if i % (10 * report) == 0:
                sys.stdout.write("|")
                sys.stdout.flush()
            elif i % report == 0:
                sys.stdout.write(".")
                sys.stdout.flush()
            for format, file in formats_files:
                file.write(getattr(self, format)(scene))
        for format, file in formats_files:
            file.close()
        print 'done'
            
    def stream_format(self, format):
        supported_formats = self.list_formats()
        filename = self.tag + "." + getattr(self, format + "_ext")
        if os.path.exists(filename):
            f = open(filename, 'r')
            return f
        else:
            getattr(self, 'format_' + format + '_header')() # it might initialize stuff
            if not format in supported_formats:
                raise_("Error in stream_formats - unsupported format: " + format)
            return SceneIteratorWrapper(self.n_examples, self.problem, self.seed,  getattr(self, 'format_' + format))
            


    def format_raw(self, scene):
        return repr(scene) + "\n"

    def format_raw_header(self):
        return ""
    
    def format_img(self, scene):
        return self.image_ascii(scene) + "\n"

    def format_img_header(self):
        return ""
    
    def format_amat(self, scene):
        return self.image_ascii(scene) + " " + " ".join([str(x) for x in self.scene_properties(scene)]) + "\n"

    def format_amat_header(self):
        return "#size: %d %d \n" % (self.n_examples, self.image_length() + 7)

    def format_desc(self, scene):
        return repr(self.problem.describe(scene)) + "\n"

    def format_desc_header(self):
        return ""

    def format_text(self, scene):
        txt = self.text(scene)
        return "\n".join(txt) + "\n"
    
    def format_text_header(self):
        return ""

    def format_cmat(self, scene):
        return self.image_text_bin(scene) # no newline

    def format_cmat_header(self):
        p = self.problem
        header = str(self.n_examples)
        header += " i:" + str(p.x_res * p.y_res) + ":" + str(len(p.palette) - 1) + ":" + str(self.bits_per_color())
        header += " u:1:2:8"
        header += " i:1:" + str(len(p.palette) - 1) + ":8"
        header += " i:1:" + str(self.xpos_granularity) + ":8"
        header += " i:1:" + str(self.ypos_granularity) + ":8"
        header += " i:1:" + str(self.orientation_granularity) + ":8"
        header += " i:1:" + str(self.size_granularity) + ":8"
        header += " i:1:" + str(self.elongation_granularity) + ":8"
        return header + "\n"
#        return header.ljust(127) + "\n"



    def image_ascii(self, scene):
        v = self.problem.vector(scene)
        maximum = float(self.problem.palette and self.img_format == 'palette' and (len(self.problem.palette) - 1) or 255)
        return " ".join([str(round(100.0 * x / maximum) / 100.0) for x in v])

    def scene_properties(self, scene):
        p = self.problem
        shape = scene.shapes[0]
        elong = (log(shape.elongation()) / self.elongation_sat / 2.0) + 0.5
        return [int(x) for x in
                [{image.RectangleImager: 0,
                  image.EllipseImager: 1,
                  image.TriangleImager: 2}[shape.__class__],
                 shape.color,
                 shape.x * self.xpos_granularity,
                 shape.y * self.ypos_granularity,
                 shape.angle / 2 / pi * self.orientation_granularity,
                 shape.area() * self.size_granularity,
                 min(max(elong, 0), 1) * self.elongation_granularity]]

    def bits_per_color(self):
        p = self.problem
        ncolors = len(p.palette)
        if self.compress:
            return int(ceil(log(ncolors) / log(2)))
        else:
            return 8

    def image_text_bin(self, scene):
        p = self.problem
        if self.img_format == 'palette':
            if p.palette:
                nbits = self.bits_per_color()
                img = scene.matrix(p.x_res, p.y_res).copy()
                if nbits == 8:
                    img_s = img.tostring()
                else:
                    img = img.resize((p.x_res * p.y_res, ))
                
                    if nbits == 2:
                        img_compressed = compress_array_2bits(img)
                    else:
                        img_compressed = compress_array(img, nbits)
                    
                    img_s = img_compressed.tostring()

                for i, attribute in enumerate(self.scene_properties(scene)):
                    img_s += chr(attribute)
                     
                return img_s
            else:
                raise 'image_text_bin: there must be a palette'
        else:
            raise 'image_text_bin: rgb format is unsupported'

        return img

    def image_length(self):
        p = self.problem
        return p.x_res * p.y_res

    def build_filename(self, type, tag=None):
        tag = tag or self.tag
        if tag:
            file_name = os.path.join(self.data_directory, tag + "." + type)
        else:
            file_name = os.path.join(self.data_directory, type)
        return file_name
    
    def open(self, type, mode):
        f = open(self.build_filename(type), mode)
        return f

    def setup_viewing(self):
        p = self.problem
        init()
        screen = display.set_mode([p.x_res_view, p.y_res_view])
        return screen

    def view(self, *indices):
#        indices = [int(index) for index in indices]
        indices = [x for x in indices]
        go_to_end = (indices == [])
        screen = self.setup_viewing()
        i = 0
        for scene in self.stream():
            if indices and not i == int(indices[0]):
                i = i + 1
                continue
            if not go_to_end and not indices:
                break
            
            screen.blit(self.problem.surface(scene), (0,0))

            props = self.scene_properties(scene)

            props = [['rect', 'ell', 'tri'][props[0]],
                     props[1],
                     1.0 * props[2] / self.xpos_granularity,
                     1.0 * props[3] / self.ypos_granularity,
                     int(360 * props[4] / self.orientation_granularity),
                     1.0 * props[5] / self.size_granularity]
            
            print i, props

            if indices:
                del indices[0]
            if indices:
                try:
                    int(indices[0])
                except Exception:
                    print indices[0]
                    del indices[0]
                    
            display.update()
            c = sys.stdin.readline()
            if c.strip() == 'q':
                break
            i = i + 1
        return True

