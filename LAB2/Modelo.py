from math import sqrt
import random
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
PURPLE = color(20, 12, 31)

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
      [PURPLE for x in range(self.width)] 
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

  
  def estrellas(self):
    for x in range(0, 300):
      self.point(random.randint(0, 600), random.randint(0, 600), WHITE)
  
  def shader(self, A, B, C, intensity, x, y):
    #1 Sur America
    center_x, center_y = 200, 300
    r1 = 300
    r2 = 1500

    if ((x - center_x)**2)/r1 + ((y - center_y)**2)/r2 < 1:
      r = round(11 * intensity)
      g = round(163 * intensity)
      b = round(3 * intensity)
    
      return color(r, g, b)

    #2 Sur America
    center_x, center_y = 215, 240
    r1 = 200
    r2 = 1200

    if ((x - center_x)**2)/r1 + ((y - center_y)**2)/r2 < 1:
      r = round(11 * intensity)
      g = round(163 * intensity)
      b = round(3 * intensity)
    
      return color(r, g, b)

    #3 Sur America
    center_x, center_y = 225, 210
    r1 = 50
    r2 = 1200

    if (((x - center_x)**2)/r1) + ((y - center_y)**2)/r2 < 1:
      r = round(11 * intensity)
      g = round(163 * intensity)
      b = round(3 * intensity)
    
      return color(r, g, b)

    #4 Sur America  
    center_x, center_y = 220, 270
    r1 = 700
    r2 = 400

    if ((x - center_x)**2)/r1 + ((y - center_y)**2)/r2 < 1:
      r = round(11 * intensity)
      g = round(163 * intensity)
      b = round(3 * intensity)
    
      return color(r, g, b)

    #Centro America
    center_x, center_y = 190, 340
    r1 = 30
    r2 = 300

    if ((x - center_x)**2)/r1 + ((y - center_y)**2)/r2 < 1:
      r = round(11 * intensity)
      g = round(163 * intensity)
      b = round(3 * intensity)
    
      return color(r, g, b)

    #Norte America
    center_x, center_y = 180, 375
    r1 = 800
    r2 = 500

    if ((x - center_x)**2)/r1 + ((y - center_y)**2)/r2 < 1:
      r = round(11 * intensity)
      g = round(163 * intensity)
      b = round(3 * intensity)
    
      return color(r, g, b)

    #Norte America 2
    center_x, center_y = 180, 430
    r1 = 10000
    r2 = 1500

    if ((x - center_x)**2)/r1 + ((y - center_y)**2)/r2 < 1:
      r = round(11 * intensity)
      g = round(163 * intensity)
      b = round(3 * intensity)
    
      return color(r, g, b)

    #Alaska
    center_x, center_y = 305, 455
    r1 = 2500
    r2 = 300

    if ((x - center_x)**2)/r1 + ((y - center_y)**2)/r2 < 1:
      r = round(11 * intensity)
      g = round(163 * intensity)
      b = round(3 * intensity)
    
      return color(r, g, b)

    #Europa
    center_x, center_y = 400, 400
    r1 = 5000
    r2 = 1500

    if ((x - center_x)**2)/r1 + ((y - center_y)**2)/r2 < 1:
      r = round(11 * intensity)
      g = round(163 * intensity)
      b = round(3 * intensity)
    
      return color(r, g, b)

    #Europa 2
    center_x, center_y = 460, 380
    r1 = 1500
    r2 = 5000

    if ((x - center_x)**2)/r1 + ((y - center_y)**2)/r2 < 1:
      r = round(11 * intensity)
      g = round(163 * intensity)
      b = round(3 * intensity)
    
      return color(r, g, b)

    #Europa 3
    center_x, center_y = 400, 360
    r1 = 300
    r2 = 800

    if ((x - center_x)**2)/r1 + ((y - center_y)**2)/r2 < 1:
      r = round(11 * intensity)
      g = round(163 * intensity)
      b = round(3 * intensity)
    
      return color(r, g, b)

    #Africa
    center_x, center_y = 350, 300
    r1 = 800
    r2 = 4500

    if ((x - center_x)**2)/r1 + ((y - center_y)**2)/r2 < 1:
      r = round(11 * intensity)
      g = round(163 * intensity)
      b = round(3 * intensity)
    
      return color(r, g, b)

    #Africa 2
    center_x, center_y = 320, 330
    r1 = 2500
    r2 = 1000

    if ((x - center_x)**2)/r1 + ((y - center_y)**2)/r2 < 1:
      r = round(11 * intensity)
      g = round(163 * intensity)
      b = round(3 * intensity)
    
      return color(r, g, b)

    #Africa 3
    center_x, center_y = 370, 250
    r1 = 500
    r2 = 2500

    if ((x - center_x)**2)/r1 + ((y - center_y)**2)/r2 < 1:
      r = round(11 * intensity)
      g = round(163 * intensity)
      b = round(3 * intensity)
    
      return color(r, g, b)

    #Africa 4
    center_x, center_y = 360, 210
    r1 = 500
    r2 = 100

    if ((x - center_x)**2)/r1 + ((y - center_y)**2)/r2 < 1:
      r = round(11 * intensity)
      g = round(163 * intensity)
      b = round(3 * intensity)
    
      return color(r, g, b)

    #Africa 5
    center_x, center_y = 360, 300
    r1 = 1000
    r2 = 300

    if ((x - center_x)**2)/r1 + ((y - center_y)**2)/r2 < 1:
      r = round(11 * intensity)
      g = round(163 * intensity)
      b = round(3 * intensity)
    
      return color(r, g, b)

    #Agua del planeta
    if A.y > 100:
      r = round(0 * intensity)
      g = round(103 * intensity)
      b = round(255 * intensity)
    
      return color(r, g, b)

    else: 

      r = round(0 * intensity)
      g = round(103 * intensity)
      b = round(255 * intensity)

      return color(r, g, b)


  def shader1(self, A, B, C, intensity, x, y):
    if A.y > 100:
      r = round(136 * intensity)
      g = round(132 * intensity)
      b = round(131 * intensity)
    
      return color(r, g, b)

    else: 

      r = round(136 * intensity)
      g = round(132 * intensity)
      b = round(131 * intensity)

      return color(r, g, b)

  #Llenado de triangulos
  def triangle(self, A, B, C, intensity, shader, color = None):
      #Triangulo más pequeño dentro del poligono
      xmin, xmax, ymin, ymax = bbox(A, B, C)
      
      for x in range(xmin, xmax + 1):
          for y in range(ymin, ymax + 1):
              P = V2(x, y)
              w, v, u = barycentric(A, B, C, P)
              
              if w < 0 or v < 0 or u < 0:
                  continue
                
              z = A.z * w + B.z * v + C.z * u

              if shader == 1:
                color = self.shader(A, B, C, intensity, x, y)
              
              elif shader == 2:
                color = self.shader1(A, B, C, intensity, x, y)

              if z > self.zbuffer[x][y]:
                  self.zbuffer[x][y] = z
                  self.point(x, y, color)

  def load(self, filename, translate, scale, shader):
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
          
          grey = round(100 * intensity)

          if grey < 0:
              continue
          
          self.triangle(A, B, C, intensity, shader, color = color(grey, grey, grey))

r = Renderer(600, 600)
#r.triangle(V2(10, 70),  V2(50, 160), V2(70, 80))
#r.triangle(V2(180, 50), V2(150, 1),  V2(70, 180))
#r.triangle(V2(180, 150), V2(120, 160), V2(130, 180))
r.estrellas()
r.load('LAB2/sphere.obj', (1, 1, 1), (300, 300, 200), 1)
r.load('LAB2/sphere.obj', (1, 5, 1), (100, 100, 200), 2)
r.display('LAB2/model.bmp')
