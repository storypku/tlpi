def lazyproperty(func):
    name = lazyproperty.prefix + func.__name__
    @property
    def lazy(self):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            value = func(self)
            setattr(self, name, value)
            return value
    return lazy

lazyproperty.prefix = "_lazy_"

import math

class Circle:
    """Demonstrate the use of lazily computed properties. Fixed the possible
    downside that the computed value becomes mutable after it's created."""
    def __init__(self, radius):
        self.radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        lazy_generator = tuple(k for k in self.__dict__
                                if k.startswith(lazyproperty.prefix))
        for k in lazy_generator:
            del self.__dict__[k]
        self._radius = value

    @radius.deleter
    def radius(self):
        raise AttributeError("Can't delete attribute")

    @lazyproperty
    def area(self):
        print("Computing area")
        return math.pi * self.radius ** 2

    @lazyproperty
    def perimeter(self):
        print("Computing perimeter")
        return 2 * math.pi * self.radius

