
from registry import *

class Dataset(Registered):

    __attributes__ = ['n_examples',
                      'data_directory',
                      'tag',
                      'seed']

    def stream(self):
        pass

    def view(self):
        pass

    def list_formats(self):
        pass

    def write_formats(self, formats):
        pass
    
