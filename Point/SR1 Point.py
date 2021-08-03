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
                 
    
r = Renderer(1024, 768)
r.glClearColor(255,255,255)
r.glClear()

r.Color(0,0,0)

r.glViewPort(100, 100, 400, 400)
r.glVertex(-1, 0.99, color(0, 0, 0))
r.glVertex(-1, 0.5, color(0, 0, 0))
r.glVertex(0.1, 0.5, color(0, 0, 0))

r.glFinish('point.bmp')