import struct

class V3(object):
    def __init__(self, x, y, z =  None):
        self.x = x
        self.y = y
        self.z = z
        
    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
    
    def __repr__(self):
        return "V3(%s, %s, %s)" % (self.x, self.y, self.z)

class V2(object):
    def __init__(self, x, y =  None):
        self.x = x
        self.y = y
        
    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
    
    def __repr__(self):
        return "V2(%s, %s)" % (self.x, self.y)
    
def ccolor(v):
    return max(0, min(255, int(v)))
    
class color(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    
    def __repr__(self):
        b = ccolor(self.b)
        g = ccolor(self.g)
        r = ccolor(self.r)
        
        return "color(%s, %s, %s)" % (r, g, b)
    
    def toBytes(self):
        b = ccolor(self.b)
        g = ccolor(self.g)
        r = ccolor(self.r)
        
        return bytes([b, g, r])
    
    def __add__(self, other):
        r = ccolor(self.r + other.r)
        g = ccolor(self.g + other.g)
        b = ccolor(self.b + other.b)
        
        return color(r, g, b)
    
    def __mul__(self, k):
        r = ccolor(self.r * k)
        g = ccolor(self.g * k)
        b = ccolor(self.b * k)
        
        return color(r, g, b)

def bbox(A, B, C):
    xs = [A.x, B.x, C.x]
    xs.sort()
    ys = [A.y, B.y, C.y]
    ys.sort()
    return round(xs[0]), round(xs[-1]), round(ys[0]), round(ys[-1])
    
def char(c):
    return struct.pack('=c', c.encode('ascii'))
    
def word(w):
    #short
    return struct.pack('=h', w)

def dword(dw):
    #long
    return struct.pack('=l', dw)

def cross(v0, v1):
    cx = v0.y * v1.z - v0.z * v1.y
    cy = v0.z * v1.x - v0.x * v1.z
    cz = v0.x * v1.y - v0.y * v1.x
    return V3(cx, cy, cz)

def barycentric(A, B, C, P):    
    bary = cross(
        V3(C.x - A.x, B.x - A.x, A.x - P.x),
        V3(C.y - A.y, B.y - A.y, A.y - P.y)
    )

    if abs(bary.z) < 1:
        return -1, -1, -1

    return (
    1 - (bary.x + bary.y) / bary.z,
    bary.y / bary.z,
    bary.x / bary.z
    )

def sub(v0, v1):
    return V3(
        v0.x - v1.x,
        v0.y - v1.y,
        v0.z - v1.z
    )

def length(v0):
    return (v0.x**2 + v0.y**2 + v0.z**2) ** 0.5

def norm(v0):
    l = length(v0)
    
    if l == 0:
        return V3(0, 0, 0)
    
    return V3(
        v0.x / l,
        v0.y / l,
        v0.z / l
    )

def mul(v0, k):
    return V3(v0.x * k, v0.y * k, v0.z *k)

def sum(v0, v1):
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def dot(v0, v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def matrix_multiply(M1, M2):
    result = [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*M2)] for X_row in M1]
    return result

black = color(0, 0, 0)
white = color(255, 255, 255)

def writeBMP(filename, width, height, pixels):
    f = open(filename, 'bw')
    
    #File header
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + 3*(width * height)))
    f.write(dword(0))
    f.write(dword(14 + 40))        
    
    #Info Header
    f.write(dword(40))
    f.write(dword(width))
    f.write(dword(height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword((width * height) * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    
    #Mapa Bits
    for y in range(height):
        for x in range(width):
            try:
                f.write(pixels[y][x].toBytes())
            except:
                pass
    
    f.close()

def reflect(I, N):
    return norm(sub(I, mul(N, 2 * dot(I, N))))

def refract(I, N, refraction_index):
    cosi = -max(-1, min(1, dot(I, N)))
    etai = 1
    etat = refraction_index
    
    if cosi < 0:
        cosi = -cosi
        etai, etat = etat, etai
        N = mul(N, -1)
    
    eta = etai/etat
    k = 1 - eta**2 * (1 - cosi**2)
    if k < 0:
        return None
    
    return norm(sum(
            mul(I, eta),
            mul(N, (eta * cosi) + k**0.5)
        ))

class Material(object):
    def __init__(self, diffuse, albedo, spec, refractive_index = 0, texture = None):
        self.albedo = albedo
        self.diffuse = diffuse
        self.spec = spec
        self.refractive_index = refractive_index
        self.texture = texture

class Intersect(object):
    def __init__(self, distance, point, normal, text_coords = None):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.text_coords = text_coords

class Light(object):
    def __init__(self, position, intensity, color):
        self.position = position
        self.intensity = intensity
        self.color = color

class Texture(object):
    def __init__(self, path):
        self.path = path
        self.read()
    
    def read(self):
        image = open(self.path, 'rb')
        
        image.seek(10)
        headerSize = struct.unpack('=l', image.read(4))[0]

        image.seek(18)
        self.width = struct.unpack('=l', image.read(4))[0]
        self.height = struct.unpack('=l', image.read(4))[0]
        image.seek(headerSize)
        self.pixels = []
        
        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1))
                g = ord(image.read(1))
                r = ord(image.read(1))
                self.pixels[y].append(color(r, g, b))
        image.close()
        
    def get_color(self, tx, ty):
        x = int(tx * self.width - 1)
        y = int(ty * self.height - 1)
        try:
            return self.pixels[y][x]
        except:
            return color(255, 255, 255)

def Transform(v, translate, scale):
        return V3(
            ((v[0] + translate[0]) * scale[0]),
            ((v[1] + translate[1]) * scale[1]),
            ((v[2] + translate[2]) * scale[2])
        )
