from lib import *

class Plane(object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = norm(normal)
        self.material = material

    def ray_intersect(self, orig, direction):
        denom = dot(direction, self.normal)

        if abs(denom) > 0.01:
            t = dot(self.normal, sub(self.position, orig)) / denom
            if t > 0:
                hit = sum(orig, mul(direction, t))

                return Intersect(distance = t,
                                 point = hit,
                                 normal = self.normal)

        return None
