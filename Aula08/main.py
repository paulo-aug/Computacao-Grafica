import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL.GLU import *
import math


def carregar_shader(nome):
    with open(nome) as f:
        return f.read()


def desenhar_cubo():

    glBegin(GL_QUADS)

    # Frente
    glNormal3f(0,0,1)
    glVertex3f(-1,-1,1)
    glVertex3f(1,-1,1)
    glVertex3f(1,1,1)
    glVertex3f(-1,1,1)

    # Trás
    glNormal3f(0,0,-1)
    glVertex3f(-1,-1,-1)
    glVertex3f(-1,1,-1)
    glVertex3f(1,1,-1)
    glVertex3f(1,-1,-1)

    # Esquerda
    glNormal3f(-1,0,0)
    glVertex3f(-1,-1,-1)
    glVertex3f(-1,-1,1)
    glVertex3f(-1,1,1)
    glVertex3f(-1,1,-1)

    # Direita
    glNormal3f(1,0,0)
    glVertex3f(1,-1,-1)
    glVertex3f(1,1,-1)
    glVertex3f(1,1,1)
    glVertex3f(1,-1,1)

    # Topo
    glNormal3f(0,1,0)
    glVertex3f(-1,1,-1)
    glVertex3f(-1,1,1)
    glVertex3f(1,1,1)
    glVertex3f(1,1,-1)

    # Base
    glNormal3f(0,-1,0)
    glVertex3f(-1,-1,-1)
    glVertex3f(1,-1,-1)
    glVertex3f(1,-1,1)
    glVertex3f(-1,-1,1)

    glEnd()


if not glfw.init():
    raise Exception("Erro ao iniciar GLFW")

janela = glfw.create_window(800,600,"Cubo",None,None)

glfw.make_context_current(janela)

program = compileProgram(
    compileShader(carregar_shader("vertex_shader.glsl"), GL_VERTEX_SHADER),
    compileShader(carregar_shader("fragment_shader.glsl"), GL_FRAGMENT_SHADER)
)

glUseProgram(program)

locTempo = glGetUniformLocation(program,"tempo")
locShininess = glGetUniformLocation(program,"shininess")

shininess = 8.0

glEnable(GL_DEPTH_TEST)

while not glfw.window_should_close(janela):

    glfw.poll_events()

    # Exercício 2
    if glfw.get_key(janela, glfw.KEY_UP) == glfw.PRESS:
        shininess += 1

    if glfw.get_key(janela, glfw.KEY_DOWN) == glfw.PRESS:
        shininess -= 1

    shininess = max(2.0, min(128.0, shininess))

    tempo = glfw.get_time()

    glUniform1f(locTempo, tempo)
    glUniform1f(locShininess, shininess)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45,800/600,0.1,100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(0,0,-5)

    glRotatef(tempo*30,1,1,0)

    desenhar_cubo()

    glfw.swap_buffers(janela)

glfw.terminate()