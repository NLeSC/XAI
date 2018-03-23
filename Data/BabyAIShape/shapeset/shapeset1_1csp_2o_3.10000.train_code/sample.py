
from random import Random
from utils import *
from math import *


#==========================================================
def samplerize(v):
    if isinstance(v, Sampler):
        return v
    else:
        return ConstantSampler(v)


#==========================================================
class Sampler(object):

    def __init__(self, rng = None):
        if rng != None:
            self.rng = rng
        else:
            self.rng = Random()
    
    def generate(self):
        """
        Generate a value according to some underlying distribution.
        """
        raise "The 'generate' method must be overriden by " + self.__class__.__name__ + "."

    def can_produce(self, value):
        """
        Returns True iff this sampler can produce the given value.
        """
        raise "The 'can_produce' method must be overriden by " + self.__class__.__name__ + "."

    def set_seed(self, seed):
        self.rng.seed(seed)


#==========================================================
class MultiSampler(Sampler):

    def __init__(self, samplers):
        Sampler.__init__(self, None)
        self.samplers = samplers

    def generate(self):
        return [sampler.generate() for sampler in self.samplers]

    def can_produce(self, value):
        return [1 for sampler in self.samplers if not sampler.can_produce(value)] == []

    def __repr__(self):
        return "Multi(" + ", ".join([repr(sampler) for sampler in self.samplers]) + ")"

#==========================================================
class UniformSampler(Sampler):
    
    def __init__(self, min, max, rng = None):
        Sampler.__init__(self, rng)
        if min >= max:
            raise "The range must be nonempty: " + repr([min, max])
        self.min = min
        self.max = max

    def generate(self):
        ans = self.rng.uniform(self.min, self.max)
        return ans

    def can_produce(self, value):
        return value >= self.min and value <= self.max

    def __repr__(self):
        return "Uniform(" + repr(self.min) + ", " + repr(self.max) + "; " + repr(self.rng) + ")"
    

#==========================================================
class IntUniformSampler(UniformSampler):
    
    def _init__(self, min, max, rng = None):
        Sampler.__init__(self, rng)
        UniformSampler.__init__(self, min, max+1)
        
    def generate(self):
        ans = UniformSampler.generate(self)
        return int(ans)

    def can_produce(self, value):
        return value == int(value) and UniformSampler.can_produce(self, value)

    def __repr__(self):
        return "IntUniform(" + repr(int(self.min)) + ", " + repr(int(self.min + self.amp - 1)) + ")"


#==========================================================
class UniformFnSpaceSampler(UniformSampler):
    """
    Samples uniformly from fn-space and converts back the
    sample to normal space using the inverse of fn. For
    example, UniformFnSpaceSampler(0.5, 2, log, exp) samples
    uniformly in log-space so samples come equiprobably
    in the [0.5, 1] range or in the [1,2] range.
    """

    def __init__(self, min, max, fn, invfn, rng = None):
        UniformSampler.__init__(self, fn(min), fn(max), rng)
        self.fn = fn
        self.invfn = invfn

    def generate(self):
        return self.invfn(UniformSampler.generate(self))

    def can_produce(self, value):
        return UniformSampler.can_produce(self, fn(value))


#==========================================================
def __square__(x):
    return x*x

class QuadraticSampler(UniformFnSpaceSampler):
    def __init__(self, min, max, rng = None):
        UniformFnSpaceSampler.__init__(self, min, max, sqrt, __square__, rng)


#==========================================================
class LogSpaceSampler(UniformFnSpaceSampler):
    def __init__(self, min, max, rng = None):
        UniformFnSpaceSampler.__init__(self, min, max, log, exp, rng)


#==========================================================
class MultiUniformSampler(Sampler):
    
    def __init__(self, ranges, rng = None):
        Sampler.__init__(self, rng)
        [error("The ranges must be nonempty.") for x,y in ranges if x >= y]
        self.ranges = [(min,max-min) for (min,max) in ranges]

    def generate(self):
        ans = [self.rng.random() * amp + min for (min,amp) in self.ranges]
        return ans

    def can_produce(self, values):
        return [1 for (x, (min, amp)) in zip(values, self.ranges) if x < min or x >= (min+amp)] == []


#==========================================================
class MultiIntUniformSampler(MultiUniformSampler):
    
    def _init__(self, ranges, rng = None):
        MultiUniformSampler.__init__(self, [(min,max+1) for (min,max) in ranges], rng)
        
    def generate(self):
        ans = UniformSampler.generate(self)
        return [int(x) for x in ans]

    def can_produce(self, values):
        return [1 for x in values if x != int(x)] == [] and MultiUniformSampler.can_produce(self, values)


#==========================================================
class BandsSampler(Sampler):

    def __init__(self, bands, rng = None):
        Sampler.__init__(self, rng)
        [raise_("Bands must be disjoint and in order.")
         for x,y in zip([z[1] for z in bands[:-1]], [z[0] for z in bands[1:]])
         if x >= y]
        [raise_("Each band must be nonempty.") for x,y in bands if x >= y]
        lengths = [x[1] - x[0] for x in bands]
        range = sum(lengths)
        self.range = range
        self.bands = bands

    def generate(self):
        targ = self.rng.random() * self.range
        for min,max in self.bands:
            interval = max-min
            if interval >= targ:
                return min + targ
            else:
                targ = targ - interval
        raise "This line should never be reached..."


#==========================================================
class ChoiceSampler(Sampler):

    def __init__(self, *samplers):
        """
        Initialize the choice sampler with a list of possible values
        a sample could take. Each possibility is equiprobable. If an
        element of the list is a subclass of Sampler, then a sample will
        be drawn from it and will be returned in its place.
        """
        if samplers and isinstance(samplers[-1], Random):
            rng = samplers[-1]
            samplers = samplers[:-1]
        else:
            rng = None
        Sampler.__init__(self, rng)
        self.samplers = map(samplerize, samplers)

    def generate(self):
        return self.rng.choice(self.samplers).generate()

    def can_produce(self, value):
        return [1 for sampler in self.samplers if sampler.can_produce(value)]


#==========================================================
class MixtureSampler(Sampler):

    def __init__(self, *samplers):
        """
        Works the same way as ChoiceSampler.__init__, but each entry
        is a pair where the first element is the probability that the
        second element will be returned or sampled from by generate()
        """
        if samplers and isinstance(samplers[-1], Random):
            rng = samplers[-1]
            samplers = samplers[:-1]
        else:
            rng = None
        Sampler.__init__(self, rng)

        if round(sum([prob for prob,sampler in samplers]), 10) != 1.0:
            raise "Probabilities must sum to 1."
        self.samplers = []
        acc = 0
        for prob, sampler in samplers:
            acc = acc + prob
            self.samplers.append((acc, samplerize(sampler)))

    def generate(self):
        idx = self.rng.random()
        sampler = scan(self.samplers, idx)
        return sampler.generate()

    def can_produce(self, value):
        return [1 for (prob, sampler) in self.samplers if sampler.can_produce(value)]


#==========================================================
class ConstantSampler(Sampler):
    
    def __init__(self, value):
        Sampler.__init__(self, None)
        self.value = value

    def generate(self):
        return self.value

    def can_produce(self, value):
        return value == self.value

    def __repr__(self):
        return "Constant(" + repr(self.value) + ")"



#==========================================================
class ConstrainedSampler(Sampler):
    def __init__(self, sampler, rng = None):
        Sampler.__init__(self, rng)
        self.sampler = sampler
            
    @staticmethod
    def valid(a):
        raise "Must be overriden."

    def generate(self):
        ans = self.sampler.generate()
        if self.valid(ans):
            return ans
        else:
            return self.generate()

    def can_produce(self, value):
        return self.valid(value) and self.sampler.can_produce(value)


