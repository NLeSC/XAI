
from utils import *
from sample import *


class Value:

    @classmethod
    def generate(cls):
        """
        Generate a random value.
        """
        pass

    @classmethod
    def generator_exact(cls):
        """
        Yield a generator to generate exact stuff with.
        """
        pass


    @classmethod
    def from_exact(cls, exact):
        pass

    @classmethod
    def from_binary(cls, binary):
        pass

    @classmethod
    def from_english(cls, english):
        pass


    def __init__(self):
        """
        Default constructor.
        """
        pass


    def exact(self):
        """
        Exact value of the property (real, tuple, etc.).
        """
        pass

    def binary(self):
        """
        Binary representation of the property.
        """
        pass

    def english(self):
        """
        English representation of the property.
        """
        pass

    def extra(self):
        pass

    def __str__(self):
        return "Value(" + ", ".join([str(self.exact()), str(self.binary()), str(self.english())]) + ")"



class TableValue(Value):

    __probs__ = []
    __table__ = []
    __rng__ = None

    @classmethod
    def __from__(cls, value, column):
        table = cls.__table__
        idx = cls.__index__(value, column)
        if idx != None:
            self = cls()
            def python_sucks(i):
                if column == i:
                    return value
                else:
                    return table[idx][i].generate()
            self._values = [python_sucks(i) for i in xrange(len(table[0]))]
            return self
        else:
            return None

    @classmethod
    def __index__(cls, value, column):
        table = cls.__table__
        i = 0
        for entry in table:
            if entry[column].can_produce(value):
                return i
            i = i + 1
        return None

    @classmethod
    @cacheresult
    def __idxgen__(cls):
        rng = cls.__rng__ and [cls.__rng__] or []
        return MixtureSampler(*(zip(cls.__probs__, cls.__table__) + rng))

    @classmethod
    @cacheresult
    def generator_exact(cls):
        rng = cls.__rng__ and [cls.__rng__] or []
        return MixtureSampler(*(zip(cls.__probs__, [entry[0] for entry in cls.__table__]) + rng))

    @classmethod
    def generate(cls):
        table = cls.__table__
        entry = cls.__idxgen__().generate()
        self = cls()
        self._values = [sampler.generate() for sampler in entry]
        return self

    @classmethod
    def from_exact(cls, exact):
        return cls.__from__(exact, 0)

    @classmethod
    def from_binary(cls, binary):
        return cls.__from__(binary, 1)

    @classmethod
    def from_english(cls, english):
        return cls.__from__(english, 2)

    def exact(self):
        return self._values[0]

    def binary(self):
        return self._values[1]

    def english(self):
        return self._values[2]

    def extra(self):
        return self._values[3:]



def TableValueClass(table, rng = None):
    class TV(TableValue):
        __rng__ = rng
    TV.__table__ = [[samplerize(element) for element in entry[1:]] for entry in table]
    TV.__probs__ = [entry[0] for entry in table]
    return TV


def ValueSampler(Sampler):

    def __init__(self, cls):
        self.table_value_class = cls

    def generate(self):
        val = self.table_value_class.generate()
        return val.exact()

    def can_produce(self, value):
        return self.table_value_class.from_exact(value) != None



def equiprob(s):
    l = len(s)
    if s:
        if isinstance(s[0], tuple):
            return [(1./l ,) + a for a in s]
        elif isinstance(s[0], list):
            return [[1./l] + a for a in s]
    else:
        return []
    

def removeprob(s, i):
    norm = 1 - s[i][0]
    s[i][0] = 0
    for j in xrange(len(s)):
        s[j][0] = s[j][0] / norm
    return s

