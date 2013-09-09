class Integer:
    def __init__(self, name):
        self.name = name

    def __get___(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError("Expected an int")
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

class Point:
    x = Integer("x")
    y = Integer("y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

if __name__ == "__main__":
    p = Point(3, 4)
    print(p.x)  # Or: Point.x.__get___(p, Point)
    p.x = 5     # Or: Point.x.__set__(p, 5)
    try:
        p.x = 2.3
    except TypeError as e:
        print(e)
