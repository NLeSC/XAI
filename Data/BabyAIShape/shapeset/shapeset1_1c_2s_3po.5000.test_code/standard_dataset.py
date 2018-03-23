
from dataset import *
from registry import *
from pygame import *
from utils import *
import sys
import os
import re

import grammar_v5 as grammar
import text_encode as encode
encode.globals_init()

class SceneIterator:

    def __init__(self, n, gen, seed):
        gen.set_seed(seed)
        grammar.reseed_grammar(seed)
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


class SceneIteratorFromFile:

    def __init__(self, problem, rawfile, textfile = None):
        self.problem = problem
        self.rawfile = open(rawfile, 'r')
        if textfile:
            self.textfile = open(textfile, 'r')
        else:
            self.textfile = None

    def __iter__(self):
        return self

    def next(self):
        scene = self.problem.load(self.rawfile.next())
        if self.textfile:
            scene.text = self.textfile.next()[:-1]
        return scene


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
    


class StandardDataset(Dataset):

    __attributes__ = ['problem',
                      'dict_n_examples',
                      ('dict_seed', None),
                      ('dict_file', None),
                      ('raw_ext', 'raw'),
                      ('img_ext', 'img'),
                      ('img_format', 'rgb'),
                      ('desc_ext', 'desc'),
                      ('text_ext', 'txt'),
                      ('amat_ext', 'amat'),
                      ('svm_ext', 'libsvm'),
                      ('cmat_ext', 'cmat'),
                      ('compress', True)]

    def __init__(self, **args):
        Dataset.__init__(self, **args)
        self.make_gram_dictionaries()
        encode.read_file_info_from_args(answer_words = self.problem.answer_words,
                                        question_words = self.problem.question_words,
                                        gram_list = self.problem.gram_dictionaries[0][0],
                                        gram_index = self.problem.gram_dictionaries[0][1],
                                        number_words_max = self.problem.number_words_max)

    def stream(self, n_examples = None):
        raw = self.build_filename(self.raw_ext)
        txt = self.build_filename(self.text_ext)
        if os.path.exists(raw):
            return SceneIteratorFromFile(self.problem, raw, os.path.exists(txt) and txt or None)
        
        if not n_examples:
            n_examples = self.n_examples
            
        if self.problem.language_real_question['location_hor'] and sum(self.problem.language_real_question.values()) == 1:
            return ConstrainedSceneIterator(n_examples,
                                            self.problem,
                                            self.seed,
                                            lambda scene, p=self.problem: [1 for shape in scene.shapes if p.__value_cls__()['x'].from_exact(shape.x).english() == 'NA'] == [])
        elif self.problem.language_real_question['location_vert'] and sum(self.problem.language_real_question.values()) == 1:
            return ConstrainedSceneIterator(n_examples,
                                            self.problem,
                                            self.seed,
                                            lambda scene, p=self.problem: [1 for shape in scene.shapes if p.__value_cls__()['y'].from_exact(shape.y).english() == 'NA'] == [])
        else:
            return SceneIterator(n_examples, self.problem, self.seed)
        
    def list_formats(self):
        formats = []
        for member in dir(self):
            if member.startswith('format_'):
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
            

    def make_gram_dictionaries(self):
        p = self.problem
        if p.gram_dictionaries:
            return
        elif self.dict_file == 'file':
            encode.read_file_info(os.path.join(self.data_directory, self.tag) + ".info")
            p.question_words = encode.questionDICT
            p.answer_words = encode.answerDICT
            p.number_words_max = encode.NUMBER_WORDS_MAX
            p.gram_dictionaries = [[encode.gramLIST, encode.gramINDEX]]
            return
        elif self.dict_file:
            d = {}
            if re.match("^/.*",self.dict_file):
                dictf = self.dict_file
            else:
                dictf = os.path.join(self.data_directory, self.dict_file)
            execfile(dictf, globals(), d)
            d = D(**d)
            p.question_words = d.question_words
            p.answer_words = d.answer_words
            p.number_words_max = d.number_words_max
            p.gram_dictionaries = d.gram_dictionaries
            return
        
        print 'Generating dictionaries...'
        print "words list..."
        
        text_it = SceneIteratorWrapper(self.dict_n_examples, p, self.dict_seed, self.format_text)
        (p.question_words, p.answer_words, number_words_max) = encode.create_dictionary_from_text_stream(text_it)

        p.number_words_max = int(number_words_max * 1.1)

        def report(x):
            print str(x) + "-grams..."
            return True

        p.gram_dictionaries = [report(n) and encode.create_gramINDEX_from_text_stream(n, SceneIteratorWrapper(self.dict_n_examples, p, self.dict_seed, self.format_text))
                               for n in p.text_encodings if isinstance(n, int)]


    def format_raw(self, scene):
        return repr(scene) + "\n"

    def format_raw_header(self):
        return ""
    
    def format_img(self, scene):
        return self.image_ascii(scene) + "\n"

    def format_img_header(self):
        return ""

    def format_amat(self, scene):
        im = self.image_ascii(scene)
        t_enc = self.problem.text_encode(scene)
        encs = [im + " " + " ".join([" ".join([str(n) for n in list]) for list in t]) for t in t_enc]
        return "\n".join(encs) + "\n"

    def format_amat_header(self):
        return "#size: %d %d \n" % (self.n_examples, self.image_length() + self.encoded_text_length() + 1)

    def format_svm(self, scene):
        im_v = self.problem.vector(scene)
        maximum = float(self.problem.palette and self.img_format == 'palette' and (len(self.problem.palette) - 1) or 255)
        im_v = [round(100.0 * x / maximum) / 100.0 for x in im_v]
        txt_vs = self.problem.text_encode(scene)[0]
        v = im_v
        for txt_v in txt_vs:
            v += txt_v
        self.__svm_count__ += 1
        return str(self.__svm_count__) + " " + " ".join([str(i) + ":" + str(x) for x, i in zip(v, xrange(1, len(v)+1))]) + "\n"

    def format_svm_header(self):
        self.__svm_count__ = 0
        return "" # no header? hurray!
    
    def format_desc(self, scene):
        return repr(self.problem.describe(scene)) + "\n"

    def format_desc_header(self):
        return ""

    def format_text(self, scene):
        txt = self.problem.text(scene)
#        return "; ".join(txt) + "\n"
        return "\n".join(txt) + "\n"
    
    def format_text_header(self):
        return ""

    def format_cmat(self, scene):
        return self.image_text_bin(scene) # no newline

    def format_cmat_header(self):
        p = self.problem
        header = str(self.n_examples) + " "
        header += "i:" + str(p.x_res * p.y_res) + ":" + str(len(p.palette) - 1) + ":" + str(self.bits_per_color())
        bpte = self.bits_per_text_encoding()
        etm = self.encoded_text_maxes()
        etl = self.encoded_text_lengths(False)
        if p.language_sentence == 'oneofeach':
            n = sum(p.language_real_question.values())
        else:
            n = 1
        for dummy in xrange(n):
            header += " " + " ".join([(isinstance(enc, int) and 'i' or enc) + ":" + str(etl[enc]) + ":" + str(etm[enc]) + ":" + str(bpte[enc])
                                for enc in p.text_encodings])
            header += " u:1:" + str(len(p.answer_words) + 1) + ":8"
        return header + "\n"
#        return header.ljust(127) + "\n"



    def image_ascii(self, scene):
        v = self.problem.vector(scene)
        maximum = float(self.problem.palette and self.img_format == 'palette' and (len(self.problem.palette) - 1) or 255)
        return " ".join([str(round(100.0 * x / maximum) / 100.0) for x in v])

    def bits_per_color(self):
        p = self.problem
        ncolors = len(p.palette)
        if self.compress:
            return int(ceil(log(ncolors) / log(2)))
        else:
            return 8

    def bits_per_text_encoding(self):
        p = self.problem
        lengths = self.encoded_text_lengths()
        ret = {}
        for enc, length in lengths.items():
            if enc == 'i' or enc == 'o':
                ret[enc] = self.compress and int(ceil(log(len(p.question_words) + 1) / log(2))) or 8 # len+1 because of the case where there is no word
            elif isinstance(enc, int):
                ret[enc] = self.compress and int(ceil(log(p.histogram_ceil + 1) / log(2))) or 8
            else:
                raise "Unsupported encoding: " + enc
        return ret


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

                et = p.text_encode(scene, False)
                s = img_s
                bpte = self.bits_per_text_encoding()
                for subet in et:
                    for enc, result in zip(p.text_encodings, subet[:-1]):
                        bits = bpte[enc]
                        if bits == 8:
                            ts = numpy.array(result).tostring()
                        elif bits == 2:
                            ts = compress_array_2bits(result).tostring()
                        elif bits == 1:
                            ts = compress_array_1bit(result).tostring()
                        else:
                            ts = compress_array(result, bits).tostring()
                        s += ts
                    s += chr(subet[-1][0])
                return s
            else:
                raise 'image_text_bin: there must be a palette'
        else:
            raise 'image_text_bin: rgb format is unsupported'

        return img

    def image_length(self):
        p = self.problem
        return p.x_res * p.y_res

    def encoded_text_lengths(self, expand_onehot = True):
        p = self.problem
        lengths = {}
        grams = [x for x in p.text_encodings if isinstance(x, int)]
        for enc in p.text_encodings:
            if enc == 'i':
                lengths[enc] = p.number_words_max
            elif enc == 'o':
                lengths[enc] = p.number_words_max * (expand_onehot and len(p.question_words) or 1)
            else:
                i = grams.index(enc)
                lengths[enc] = len(p.gram_dictionaries[i][0])
        return lengths

    def encoded_text_maxes(self):
        p = self.problem
        maxes = {}
        for enc in p.text_encodings:
            if enc == 'i' or enc == 'o':
                maxes[enc] = len(p.question_words) - 1
            else:
                maxes[enc] = 1 #self.histogram_ceil
        return maxes

    def encoded_text_length(self):
        lengths = self.encoded_text_lengths()
        return sum(lengths.values())

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
            txt = self.format_text(scene)
            if indices and not i == int(indices[0]):
                i = i + 1
                continue
            if not go_to_end and not indices:
                break
            
            screen.blit(self.problem.surface(scene), (0,0))

            print i, txt
#            self.problem.text_encode(scene) # print
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

