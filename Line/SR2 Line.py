'UNIVERSIDAD DEL VALLE DE GUATEMALA'
'Gráficas por Computadora'
'Sección 10'
'Javier Alejandro Cotto Argueta 19324'

import struct
from SR3D import *

def char(c):
    return struct.pack('=c', c.encode('ascii'))
    
def word(w):
    #short
    return struct.pack('=h', w)

def dword(dw):
    #long
    return struct.pack('=l', dw)

def color(r, g, b):
    return bytes([b, g, r])

black = color(0, 0, 0)
white = color(255, 255, 255)

class Renderer(object):
    
    def __init__(self, width, height):
        self.CurrentColor = color(250, 250, 250)
        self.ClearColor = color(10, 10, 10)
        self.width = width
        self.height = height
        self.glCreateWindow(self.width, self.height)
        
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.framebuffer = [[white for x in range(self.width)]
                            for y in range(self.height)
                            ]
        self.glViewPort(0, 0, self.width, self.height)
     
    #Normalized Device Coordinates coverter
    def NDC(self, x_viewport, y_viewport):
        xw = int((x_viewport + 1) * (self.width  / 2) + self.viewportx)
        yw = int((y_viewport + 1) * (self.height / 2) + self.viewporty)
        return xw, yw

    def glViewPort(self, x, y, width, height):
        self.viewportx = x
        self.viewporty = y
        self.vwidth = width
        self.vheight = height

    def glClear(self):
        self.fill_map = [
            [self.ClearColor for y in range(self.height)]
            for x in range(self.width)
            ]
        
    def glClearColor(self, r, g, b):
        self.ClearColor = color(r, g, b)
         

    def Color(self, r, g, b):
        self.CurrentColor = color(r, g, b)
        
    def glVertex(self, x, y, color):
        x_window, y_window = self.NDC(x, y)
        self.framebuffer[x_window][y_window] = color or self.CurrentColor
        
    def glLine(self, x0, y0, x1, y1):
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0 * 2 * dx
        threshold = 0.5
        y = y0

        # y = mx + b
        points = []
        for x in range(x0, x1 + 1):
            if steep:
              points.append((y, x))
            else:
              points.append((x, y))

            offset += (dy/dx) * 2 * dx
            if offset >= threshold:
              y += 1 if y0 < y1 else -1
              threshold += 1 * 2 * dx

        for pointf in points:
            point(*pointf)
    
    #FUNCION PARA DIBUJAR CUBO                    
    def load(self, filename):
        model = Obj(filename)
        
        for face in model.caras:
            for j in range(4):
                f1 = face[j][0]
                f2 = face[(j + 1) % 4][0]
                
                v1 = model.vertices[f1 - 1]
                v2 = model.vertices[f2 - 1]
                
                #glVertex
                x1 = v1[0]
                y1 = v1[1]
                x2 = v2[0]
                y2 = v2[1]
                
                #Funcion linea a implementar
                self.glLine(x1, y1, x2, y2)
    
    def glFinish(self, filename):
        f = open(filename, 'bw')
        
        #File header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + 3*(self.width * self.height)))
        f.write(dword(0))
        f.write(dword(14 + 40))
        
        
        #Info Header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword((self.width * self.height) * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        
        #Mapa Bits
        for y in range(self.height):
            for x in range(self.width):
                f.write(self.framebuffer[y][x])
        
        f.close()
                 
    
r = Renderer(800, 800)
r.load('cube.obj')

#r.glClearColor(255,255,255)
#r.glClear()

#r.Color(0,0,0)

r.glViewPort(100, 100, 400, 400)
#r.glVertex(-1, 0.2, color(0, 0, 0))
#r.glVertex(-1, 0.5, color(0, 0, 0))
#r.glVertex(0.1, 0.5, color(0, 0, 0))

#r.line(0.01, 0.01, -0.99, -0.35)

r.glFinish('point.bmp')