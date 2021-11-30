import pygame
import numpy
from obj import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm

pygame.init()
screen = pygame.display.set_mode((1200, 720), pygame.OPENGL | pygame.DOUBLEBUF)
glClearColor(0.1, 0.2, 0.5, 1.0)
glEnable(GL_DEPTH_TEST)
clock = pygame.time.Clock()

#SHADER 1
vertex_shader = """
#version 460

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 ccolor;

uniform mat4 theMatrix;

out vec3 mycolor;

void main() 
{
gl_Position = theMatrix * vec4(position.x, position.y, position.z, 1);
mycolor = ccolor;
}
"""

fragment_shader = """
#version 460
layout(location = 0) out vec4 fragColor;

uniform int clock;
in vec3 mycolor;

void main()
{
if (mod(clock/10, 2) == 0) {
    fragColor = vec4(mycolor.xyz, 1.0f);
} else {
    fragColor = vec4(mycolor.zxy, 1.0f);
}
}
"""

cvs = compileShader(vertex_shader, GL_VERTEX_SHADER)
cfs = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
shader = compileProgram(cvs, cfs)

vertex_shader1 = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 ccolor;

uniform mat4 theMatrix;

out vec3 mycolor;

void main() 
{
gl_Position = theMatrix * vec4(position.x, position.y, position.z, 1);
mycolor = ccolor;
}
"""

fragment_shader1 = """
#version 460
layout(location = 0) out vec4 fragColor;

uniform int clock;
in vec3 mycolor;

void main()
{
  fragColor = vec4(mycolor.xxx, 5.0f);
}
"""

mesh = Obj('./Tie_FighterF.obj')

'''vertex_data = numpy.hstack((
  numpy.array(mesh.vertices, dtype=numpy.float32),
  numpy.array(mesh.normals, dtype=numpy.float32),
)).flatten()'''

vectores_object = []

for face in mesh.vfaces:
  for v in range(len(face)):
    vertex = mesh.vertices[face[v][0] - 1]
    vectores_object.extend(vertex)
            
    tvertex = mesh.tvertices[face[v][1] - 1]
    vectores_object.extend(tvertex)
                  
    normal = mesh.normals[face[v][2] - 1]
    vectores_object.extend(normal)

vectores_object = numpy.array(vectores_object, dtype = numpy.float32)        

index_data = numpy.array([[vertex[0] - 1 for vertex in face] for face in mesh.vfaces], dtype=numpy.uint32).flatten()

vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(GL_ARRAY_BUFFER, vectores_object.nbytes, vectores_object, GL_STATIC_DRAW)

vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)
glVertexAttribPointer(
  0, # location
  3, # size
  GL_FLOAT, # tipo
  GL_FALSE, # normalizados
  4 * 9, # stride
  ctypes.c_void_p(0)
)
glEnableVertexAttribArray(0)

element_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

glVertexAttribPointer(
  1, # location
  3, # size
  GL_FLOAT, # tipo
  GL_FALSE, # normalizados
  4 * 9, # stride
  ctypes.c_void_p(4 * 6)
)
glEnableVertexAttribArray(1)

glUseProgram(shader)


from math import sin
rotation = 5
zoom = 1

def render(a, rotation, zoom):
  i = glm.mat4(1)

  translate = glm.translate(i, glm.vec3(0, 0, -5))
  rotate = glm.rotate(i, glm.radians(rotation), glm.vec3(0, 1, 0))
  scale = glm.scale(i, glm.vec3(zoom, zoom, zoom))

  model = translate * rotate * scale
  view = glm.lookAt(glm.vec3(0, 0, 20), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
  projection = glm.perspective(glm.radians(45), 1200/720, 0.1, 1000.0)

  theMatrix = projection * view * model

  glUniformMatrix4fv(
    glGetUniformLocation(shader, 'theMatrix'),
    1,
    GL_FALSE,
    glm.value_ptr(theMatrix)
  )

  glViewport(0, 0, 1200, 720)

a = 0
running = True
while running:
  rotation += 1
  glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

  render(a, rotation, zoom)
  a += 1
  
  glUniform1i(
    glGetUniformLocation(shader, 'clock'),
    a
  )

  glDrawArrays(GL_TRIANGLES, 0, len(mesh.vfaces) * 3)

  pygame.display.flip()
  clock.tick(15)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:

      #Just underlined polygon
      if event.key == pygame.K_3:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

      #Fill polygon
      if event.key == pygame.K_4:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
      
      #Just Vertex Points
      if event.key == pygame.K_5:
        glPolygonMode(GL_FRONT_AND_BACK, GL_POINT)

      #change to 2nd shader
      if event.key == pygame.K_2:
        cvs = compileShader(vertex_shader1, GL_VERTEX_SHADER)
        cfs = compileShader(fragment_shader1, GL_FRAGMENT_SHADER)
        shader = compileProgram(cvs, cfs)
        glUseProgram(shader)

      #return to 1st shader
      if event.key == pygame.K_1:
        cvs = compileShader(vertex_shader, GL_VERTEX_SHADER)
        cfs = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
        shader = compileProgram(cvs, cfs)
        glUseProgram(shader)
      
      #Zoom In
      if event.key == pygame.K_i:
        if zoom <= 6:
          zoom += 1

      #Zoom Out
      if event.key == pygame.K_o:
        if zoom >= 2:
          zoom -= 1
      
      #Por alguna razón el numpad no lee la entrada de los botones
      # + Rotate Right
      if event.key == pygame.K_PLUS:
        rotation += 10
      
      #- Rotate Left
      if event.key == pygame.K_MINUS:
        rotation -= 10
