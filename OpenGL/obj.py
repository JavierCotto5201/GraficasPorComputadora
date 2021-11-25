class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()

        self.vertices = []
        self.tvertices = []
        self.normals = []
        self.vfaces = []
        self.read()

    def read(self):
        for line in self.lines:
            if line:
                try:
                    prefix, value = line.split(' ', 1)
                except:
                    prefix = ''
                if prefix == 'v':
                    vertice = list(map(float, value.split(' ')))
                    self.vertices.append(vertice)
                elif prefix == 'vt':
                    self.tvertices.append(
                      list(map(float, value.split(' ')))
                    )
                elif prefix == 'vn':
                    self.normals.append(
                      list(map(float, value.split(' '))) 
                    )
                elif prefix == 'f':
                    self.vfaces.append(
                        [list(map(int, face.split('/'))) for face in value.split(' ')]
                    )

        

    
    
    
    
    
    