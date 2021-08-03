'UNIVERSIDAD DEL VALLE DE GUATEMALA'
'Gráficas por Computadora'
'Sección 10'
'Javier Alejandro Cotto Argueta 19324'

import struct
    
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
        self.framebuffer[x][y] = color or self.CurrentColor
        
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
                 
    
r = Renderer(40, 40)
r.glClearColor(255,255,255)
r.glClear()
r.Color(0,0,0)

r.glVertex(10, 10, black)
r.glVertex(10, 11, black)
r.glVertex(11, 10, black)

r.glFinish('point.bmp')