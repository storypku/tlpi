class LazyProperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value

import math

class Circle:
    """Demonstrate the use of lazily computed properties. However, one
    possible downside is that the computed value becomes mutable after it's
    created."""
    def __init__(self, radius):
        self.radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        try:
            del self.area, self.perimeter
        except AttributeError:
            pass
        self._radius = value

    @radius.deleter
    def radius(self):
        raise AttributeError("Can't delete attribute")

    @LazyProperty
    def area(self):
        print("Computing area")
        return math.pi * self.radius ** 2

    @LazyProperty
    def perimeter(self):
        print("Computing perimeter")
        return 2 * math.pi * self.radius

