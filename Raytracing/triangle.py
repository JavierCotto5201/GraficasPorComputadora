from lib import *

class Triangle(object):
    def __init__(self, vertices, material):
        self.vertices = vertices
        self.material = material

    def ray_intersect(self, origin, direction):
        epsilon = 0.001
        v0, v1, v2 = self.vertices
        normal = cross(sub(v1, v0), sub(v2, v0))
        determinant = dot(normal, direction)

        if abs(determinant) < epsilon:
            return None

        distance = dot(normal, v0)
        t = (dot(normal, origin) + distance) / determinant
        if t < 0:
            return None

        point = sum(origin, mul(direction, t))
        u, v, w = barycentric(v0, v1, v2, point)

        if w < 0 or v < 0 or u < 0:  # 0 is actually a valid value! (it is on the edge)
            return None
        
        return Intersect(distance=distance, point=point, normal=norm(normal))