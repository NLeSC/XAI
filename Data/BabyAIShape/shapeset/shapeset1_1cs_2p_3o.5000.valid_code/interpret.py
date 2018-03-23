
from sample import *
from generate import *
from utils import *
from value import *


class AttributeInterpreter:
    
    def __init__(self, obj, assoc):
        self.__dict__['__object__'] = obj
        self.__dict__['__assoc__'] = assoc
        
    def __getattr__(self, attr):
        d = self.__dict__
        a = d['__assoc__']
        if attr == '__assoc__':
            return a
        o = d['__object__']
        if attr == '__object__':
            return o
        v = getattr(o, attr)
        if attr.startswith('_') and not attr in ['__getitem__']:
            return v
        if a.has_key(attr):
            if callable(v):
                return lambda *args: a[attr](v(*args))
            else:
                return a[attr](v)
        else:
            if callable(v):
                return lambda *args: AttributeInterpreter(v(*args), a)
            else:
                return AttributeInterpreter(v, a)

    def __setattr__(self, attr, value):
        raise "Setting attributes is not allowed."
