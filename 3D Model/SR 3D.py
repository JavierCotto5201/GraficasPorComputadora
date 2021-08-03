import struct
from SR3D import *


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


class Renderer(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.current_color = WHITE
    self.glCreateWindow()

  def glCreateWindow(self):
    self.framebuffer = [
      [BLACK for x in range(self.width)] 
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
    
  def load(self, filename, translate, scale):
    model = Obj(filename)
    
    for face in model.caras:
      vcount = len(face)

      for j in range(vcount):
        f1 = face[j][0]
        f2 = face[(j + 1) % vcount][0]

        v1 = model.vertices[f1 - 1]
        v2 = model.vertices[f2 - 1]
        
        x1 = round((v1[0] + translate[0]) * scale[0])
        y1 = round((v1[1] + translate[1]) * scale[1])
        x2 = round((v2[0] + translate[0]) * scale[0])
        y2 = round((v2[1] + translate[1]) * scale[1])

        self.line((x1, y1), (x2, y2))

r = Renderer(800, 800)
r.load('Vader.obj', (1.6, 0.5), (300, 300))
r.display('model.bmp')
