from Modelo import *
import random
from random import randint

def shader_Textura(render, **kwargs):
    w, v, u = kwargs['bar']
    tx, ty = kwargs['tex_coords']
    nA, nB, nC = kwargs['varying_normales']
    
    tcolor = render.current_texture.get_color(tx, ty)

    iA, iB, iC = [dot(n, render.light) for n in (nA, nB, nC)]
    
    intensity = w*iA + v*iB + u*iC
    
    return tcolor * intensity

def Tie_shader(render, **kwargs):
    w, v, u = kwargs['bar']
    nA, nB, nC = kwargs['varying_normales']
    A, B, C = kwargs['triangle']

    tcolor = color(57, 59, 168)
    
    iA, iB, iC = [dot(n, render.light) for n in (nA, nB, nC)]
    
    intensity = w*iA + v*iB + u*iC
    
    return tcolor * intensity *2

def Gun_shader(render, **kwargs):
    w, v, u = kwargs['bar']
    nA, nB, nC = kwargs['varying_normales']
    A, B, C = kwargs['triangle']

    tcolor = color(200, 0, 0)
    
    iA, iB, iC = [dot(n, render.light) for n in (nA, nB, nC)]
    
    intensity = w*iA + v*iB + u*iC
    
    return tcolor * intensity

def Meteor_shading(render, **kwargs):
    w, v, u = kwargs['bar']
    nA, nB, nC = kwargs['varying_normales']
    A, B, C = kwargs['triangle']

    tcolor = color(250, 250, 250)
    
    iA, iB, iC = [dot(n, render.light) for n in (nA, nB, nC)]
    
    intensity = w*iA + v*iB + u*iC
    
    return tcolor * intensity

pi = 3.14

def estrellas(render):
    for x in range(0, 300):
      render.point(random.randint(0, 990), random.randint(0, 990), white)

r = Renderer(1000, 1000)
r.lookAt(V3(0, 0, 5), V3(0, 0, 0), V3(0, 1, 0))


estrellas(r)

#LUNA BOSS
r.current_texture = Texture('./models/moon_normals.bmp')
r.light = V3(0.5, 0, 0.5)
r.load('./models/MOONF.obj', (-0.7, -0.7, -1), (0.5, 1.25, 0.25), (0, 0, 0))
r.active_shader = shader_Textura
r.draw_arrays('TRIANGLES')

#TIE FIGHTER
r.current_texture = None
r.light = V3(0, 1, 0)
r.load('./models/Tie_FighterF.obj', (0.65, 0.5, -2), (0.20, 0.20, 0.20), (0.5, -pi/5, 0))
r.active_shader = Tie_shader
r.draw_arrays('TRIANGLES')

#TIE FIGHTER
r.current_texture = None
r.light = V3(0, 1, 0)
r.load('./models/Tie_FighterF.obj', (0.35, -0.5, -1), (0.20, 0.20, 0.20), (0, -pi, 0))
r.active_shader = Tie_shader
r.draw_arrays('TRIANGLES')

#MOON GUN
r.current_texture = None
r.light = V3(0, 0, 1)
r.load('./models/alien_gun.obj', (-0.8, -0.2, 0), (0.2, 0.2, 0.2), (0, 0, 0))
r.active_shader = Gun_shader
r.draw_arrays('TRIANGLES')

#METEOR
r.current_texture = None
r.light = V3(-0.5, 0.5, 0)
r.load('./models/A2Fobj.obj', (0, 0, -10), (1, 1, 1), (0, -10, 0))
r.active_shader = Meteor_shading
r.draw_arrays('TRIANGLES')


r.display()
