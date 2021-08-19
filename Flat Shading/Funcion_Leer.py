
class Obj(object):
    
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.vertices = []
        self.caras = []
        self.read()
        
    
    def read(self):
        for line in self.lines:
            if line:
                prefix, value = line.split(' ', 1)
                
                if prefix == 'v':
                    self.vertices.append(list(map(float, value.split(' '))))
                    
                elif prefix == 'f':
                    self.caras.append([list(map(int, face.split('//'))) for face in value.split(' ')])

#FUNCION PARA DIBUJAR CUBO                    
    def load(self, filename):
        model = Obj(filename)
        
        for face in model.faces:
            vcount = len(face)
            
            for j in range(vcount):
                f1 = face[j][0]
                f2 = face[(j + 1) % 4][0]
                
                v1 = model.vertices[f1 - 1]
                v2 = model.vertices[f2 - 1]
                
                #glVertex
                x1 = round((v1[0] + translate[0]) * scale[0])
                y1 = round((v1[1] + translate[1]) * scale[1])
                x2 = round((v2[0] + translate[0]) * scale[0])
                y2 = round((v2[1] + translate[1]) * scale[1])
                
                #Funcion linea a implementar
                self.line(x1, y1, x2, y2)
    
        
#cube = Obj('cube.obj')
#print(cube.vertices)
#print(cube.caras)
    