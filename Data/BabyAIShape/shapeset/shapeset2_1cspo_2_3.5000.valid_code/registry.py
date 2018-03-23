

from utils import *


#==========================================================
class Registry(object):

    def __init__(self, **registry):
        self.__registry__ = {}
        for keyword, cls in registry.items():
            self.register(keyword, cls)

    def register(self, keyword, cls):
        """
        Register maps names to the class they correspond to.
        Use registry.register(name, class) to fill it.
        """
        self.__registry__[keyword] = cls

    def load(self, x):
        """
        Creates an object out of its representation. The representation can be:
        - A string as given by repr(object)
        - A dictionary containing {attribute: value} pairs
        Example: Registered.load({'type': 'circle', 'radius':5, 'color':(255,0,0)})
        """
        if isinstance(x, dict):
            t = x['type']
            del x['type']
            ret = self.__registry__[t](**x)
            x['type'] = t
            ret.type = x['type']
            return ret
        elif isinstance(x, str):
            Create = self.create
            return self.load(eval(x))
        elif isinstance(x, D):
            return self.load(D.__dict__)
        elif isinstance(x, Registered):
            return x
        else:
            raise "Cannot load from type: " + type(x)

    def create(self, **props):
        """
        Alternative syntax for load.
        Example: registry.create(type='circle', color='black', radius=20)
        """
        return self.load(props)

    def classof(self, keyword):
        reg = self.__registry__
        try:
            return reg[keyword]
        except KeyError:
            return None


#==========================================================
class Registered(object):
    """
    This class implements a serialization mechanism.
    """
    

    ##########################
    #### Class attributes ####
    ##########################

    """
    Defines the default value of __check_validity__ for shape instances.
    """
    __check_validity_default__ = False


    __attributes__ = []
    


    #######################
    #### Class methods ####
    #######################
    
    @classmethod
    def attributes(cls):
        """
        Returns a list of attributes for the object. Do not override it.
        Instead, declare new attributes for your subclass in __attributes__
        Example: class MyShape: __attributes__ = ['x', 'y', ('color', 'black')]
        """
        attrs = []
        while cls != Registered:
            attrs += cls.__attributes__ # if the class doesn't redefine __attributes__ there will be duplicates
            cls = cls.__base__
        return attrs
    

    ##################################
    #### Constructor and builtins ####
    ##################################
    
    def __init__(self, **desc):
        """
        Subclasses should not need to override __init__. Add attributes to __attributes__ instead.
        """
        cls = self.__class__
        attrs = self.__class__.attributes()
        str_attrs = [attr for attr in attrs if isinstance(attr, str)] + [attr[0] for attr in attrs if isinstance(attr, tuple)]
#        for attr in desc.keys():
#            if not attr in str_attrs:
#                print "Warning: unknown attribute '" + attr + "' given for " + cls.__name__ + "."
        for attr in attrs:
            if isinstance(attr, tuple):
                if not desc.has_key(attr[0]):
                    desc[attr[0]] = attr[1];
            elif isinstance(attr, str):
                if not desc.has_key(attr):
                    raise "Error: missing required attribute '" + attr + "' for " + cls.__name__ + "."
        self.__dict__.update(desc)
        self.check_validity(cls.__check_validity_default__)
        
    def __repr__(self):
        """
        The representation returned by repr is such that for an instance of
        an object called o, Registered.load(repr(o)) will return a copy of o.
        """
        cls = self.__class__
        d = {}
        if hasattr(self, 'type'):
            d['type'] = self.type
        for attr in cls.attributes():
            if isinstance(attr, str):
                d[attr] = self.__dict__[attr]
            elif isinstance(attr, tuple):
                d[attr[0]] = self.__dict__[attr[0]]
        ans = "Create(" + ", ".join([k + "=" + repr(v) for k, v in d.items()]) + ")"
        return ans

    def __str__(self):
        return repr(self)

    def __setattr__(self, k, v):
        if k.startswith("_"):
            self.__dict__[k] = v
        else:
            self.update(**{k: v}) # update checks for validity
    

    ###############################################
    #### Validity checks, cloning and updating ####
    ###############################################
    
    def check_validity(self, b):
        """
        Toggle validity checks by the class. If b = True, all property sets and updates
        will raise an exception if they make the shape invalid.
        """
        if b:
            if self.valid():
                self.__check_validity__ = b
            else:
                raise "You can only turn validity checks on if the object is in a valid state."
        else:
            self.__check_validity__ = False

    def valid(self):
        """
        Returns True if the object's attributes represent valid parameters for the object type.
        """
        return True

    def get(self, attr):
        """
        Returns the value of an attribute
        """
        return getattr(self, attr)

    def update(self, **args):
        """
        Updates properties of the object.
        Example: circle.update(radius = 10, color = 'red')
        This method modifies the object and returns it.
        """
        if self.__check_validity__:
            old_dic = copy(self.__dict__)
            self.__dict__.update(args)
            if not self.valid():
                self.__dict__ = old_dic
                raise "Update made the object's state invalid: " + repr(args)
        else:
            self.__dict__.update(args)
        return self

    def update_copy(self, **args):
        """
        Same as update(self, **args) but does not change the current object
        and returns a fresh copy instead.
        """
        return self.clone().update(**args)

