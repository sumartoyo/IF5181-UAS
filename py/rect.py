from point import Point

class Rect:
    def __init__(self, a=None, d=None):
        self.a = a if a is not None else Point()
        self.d = d if d is not None else Point()
    def __str__(self):
        return '{}:{}'.format(self.a, self.d)