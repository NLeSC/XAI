
from registry import *
from sample import *

class Problem(Registered, Sampler):

    __attributes__ = ['x_res',
                      'y_res']

## inherited from Sampler:

#     def generate(self):
#         pass

#     def can_produce(self):
#         pass

#     def set_seed(self):
#         pass


    def load(self, desc):
        pass

    def surface(self, scene):
        pass

    def vector(self, scene):
        pass

    def interpret(self, scene):
        pass

    def describe(self, scene):
        pass
