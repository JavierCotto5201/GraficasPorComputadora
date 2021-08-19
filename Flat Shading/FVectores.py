#Funciones Matriciales y Vectoriales
from collections import namedtuple


V2 = namedtuple('Point2D', ['x', 'y'])
V3 = namedtuple('Point3D', ['x', 'y', 'z'])

def p_cruz(v0, v1):
    cx = v0.y * v1.z - v0.z * v1.y
    cy = v0.z * v1.x - v0.x * v1.z
    cz = v0.x * v1.y - v0.y * v1.x

    return V3(cx, cy, cz)

def sub(v0, v1):
    
    return V3(
        v0.x - v1.x,
        v0.y - v1.y,
        v0.z - v1.z
    )

def lenght(v0):
    return (v0.x**2 + v0.y**2 + v0.z**2)**0.5


def norm(v0):
    u = lenght(v0)
    
    if u == 0:
        return V3(0, 0, 0)
    
    return  V3(
        v0.x / u,
        v0.y / u,
        v0.z / u
    )

def dot(v0, v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def barycentric(A, B, C, P):

  cx, cy, cz = p_cruz(
    V3(B.x - A.x, C.x - A.x, A.x - P.x), 
    V3(B.y - A.y, C.y - A.y, A.y - P.y)
  )

  if abs(cz) < 1:
    return -1, -1, -1

  u = cx/cz
  v = cy/cz
  w = 1 - (cx + cy)/cz

  return w, v, u

def transform2D(v, translate, scale):
        return V2(
        round((v[0] + translate[0]) * scale[0]),
        round((v[1] + translate[1]) * scale[1])
        )
    
def transform3D(v, translate, scale):
        return V3(
        round((v[0] + translate[0]) * scale[0]),
        round((v[1] + translate[1]) * scale[1]),
        round((v[2] + translate[2]) * scale[2])
        )