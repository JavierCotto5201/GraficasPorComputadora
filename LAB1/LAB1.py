'Universidad del Valle de Guatemala'
'Gráficas por Computadora Seccion 10'
'Javier Alejandro Cotto Argueta 19324'

from SR3D import *

def contornoFigura(r, listaFig):
    for v in listaFig:
        for x in range(len(v)):
            r.line(v[x][0], v[x][1], v[(x+1)%len(v)][0], v[(x+1)%len(v)][1])
            
#Método de Hundido
#Referencia: https://www.tutorialspoint.com/computer_graphics/polygon_filling_algorithm.htm
def pintarFigura(r, x ,y , color):
    n = r.width
    m = r.height
    old_color = r.framebuffer[y][x]
    if old_color == color: return
    colaPuntos = []
    colaPuntos.append((x, y))
    while not len(colaPuntos) == 0:
        i, j = colaPuntos.pop()
        if i < 0 or i >= n or j < 0 or j >= m or r.framebuffer[j][i] != old_color:
            continue
        else:
            r.point(i, j, color)
            colaPuntos.append((i + 1, j))
            colaPuntos.append((i - 1, j))
            colaPuntos.append((i, j + 1))
            colaPuntos.append((i, j - 1))

r = Renderer(800, 800)
f1 = ((165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360),
      (250, 380), (220, 385), (205, 410), (193, 383))
f2 = ((321, 335), (288, 286), (339, 251) ,(374, 302))

f3=((377, 249), (411, 197), (436, 249))

f4=((413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37),
         (660, 52), (750, 145), (761, 179), (672, 192) ,(659, 214), (615, 214),
         (632, 230), (580, 230), (597, 215), (552, 214), (517, 144), (466, 180))

f5=((682, 175), (708, 120), (735, 148), (739, 170))

figuras = [f1, f2, f3, f4, f5]
contornoFigura(r, figuras)
pintarFigura(r, 225, 405, WHITE)
pintarFigura(r, 290, 330, WHITE)
pintarFigura(r, 380, 200, WHITE)
pintarFigura(r, 150, 600, WHITE)
pintarFigura(r, 700, 150, WHITE)
r.display('imagen.bmp')


