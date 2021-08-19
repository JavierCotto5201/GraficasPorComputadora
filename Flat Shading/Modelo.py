import struct
from Funcion_Leer import *
from FVectores import *
from collections import namedtuple
from random import randrange

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #short
    return struct.pack('=h', w)

def dword(d):
    #long
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([b, g, r])

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

def bbox(A, B, C):
    xs = [A.x, B.x, C.x]
    xs.sort()
    
    ys = [A.y, B.y, C.y]
    ys.sort()
    
    return xs[0], xs[-1], ys[0], ys[-1]

V2 = namedtuple('Point2D', ['x', 'y'])
V3 = namedtuple('Point3D', ['x', 'y', 'z'])

class Renderer(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.current_color = WHITE
    self.light = V3(0, 0, 1)
    self.glCreateWindow()

  def glCreateWindow(self):
    self.framebuffer = [
      [BLACK for x in range(self.width)] 
      for y in range(self.height)
    ]
    
    self.zbuffer = [
      [-99999 for x in range(self.width)] 
      for y in range(self.height)
    ]

  def glFinish(self, filename):
    f = open(filename, 'bw')

    # File header (14 bytes)
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(14 + 40))

    # Info header (40 bytes)
    f.write(dword(40))
    f.write(dword(self.width))
    f.write(dword(self.height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    # Mapa Bits (width x height x 3 framebuffer)
    for x in range(self.height):
      for y in range(self.width):
        f.write(self.framebuffer[x][y])

    f.close()

  def display(self, filename='out.bmp'):
      self.glFinish(filename)

  def set_color(self, color):
      self.current_color = color

  def point(self, x, y, color = None):
    try:
      self.framebuffer[y][x] = color or self.current_color
    except:
      pass
    
  def line(self, start, end, color = None):
    x1, y1 = start
    x2, y2 = end

    dy = abs(y2 - y1)
    dx = abs(x2 - x1)
    steep = dy > dx

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dy = abs(y2 - y1)
    dx = abs(x2 - x1)

    offset = 0
    threshold = dx

    y = y1
    for x in range(x1, x2 + 1):
        if steep:
            self.point(y, x, color)
        else:
            self.point(x, y, color)
        
        offset += dy * 2
        if offset >= threshold:
            y += 1 if y1 < y2 else -1
            threshold += dx * 2
  
  #Llenado de triangulos
  def triangle(self, A, B, C, color = None):
      #Triangulo más pequeño dentro del poligono
      xmin, xmax, ymin, ymax = bbox(A, B, C)
      
      for x in range(xmin, xmax + 1):
          for y in range(ymin, ymax + 1):
              P = V2(x, y)
              w, v, u = barycentric(A, B, C, P)
              
              if w < 0 or v < 0 or u < 0:
                  continue
                
              z = A.z * w + B.z * v + C.z * u
              
              if z > self.zbuffer[x][y]:
                  self.zbuffer[x][y] = z
                  self.point(x, y, color)
  
  
  def load(self, filename, translate, scale):
    model = Obj(filename)
    
    for face in model.caras:
      vcount = len(face)
      
      if vcount == 3:
          f1 = face[0][0] - 1
          f2 = face[1][0] - 1
          f3 = face[2][0] - 1
          
          A = transform3D(model.vertices[f1], translate, scale)
          B = transform3D(model.vertices[f2], translate, scale)
          C = transform3D(model.vertices[f3], translate, scale)
          
          normal = norm(p_cruz(
              sub(B, A),
              sub(C, A)
              ))
          
          intensity = dot(normal, self.light)
          
          grey = round(255 * intensity)
          
          if grey < 0:
              continue
          
          self.triangle(A, B, C, color = color(grey, grey, grey))

r = Renderer(800, 800)
#r.triangle(V2(10, 70),  V2(50, 160), V2(70, 80))
#r.triangle(V2(180, 50), V2(150, 1),  V2(70, 180))
#r.triangle(V2(180, 150), V2(120, 160), V2(130, 180))
r.load('Vader.obj', (1.6, 0.5, 1), (200, 200, 500))
r.display('model.bmp')
