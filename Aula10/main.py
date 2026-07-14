import glfw
import numpy as np

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GLU import *


# --------------------------------------------------
# Carrega os shaders
# --------------------------------------------------

def carregar_shader(nome):
    with open(nome, "r") as f:
        return f.read()


program = None
modelLoc = None
colorLoc = None


# --------------------------------------------------
# Matriz de translação
# --------------------------------------------------

def matriz_translacao(x, y, z):

    return np.array([
        1,0,0,0,
        0,1,0,0,
        0,0,1,0,
        x,y,z,1
    ], dtype=np.float32)


# --------------------------------------------------
# Desenha um cubo
# --------------------------------------------------

def desenhar_cubo():

    glBegin(GL_QUADS)

    # Frente
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)

    # Trás
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5)

    # Esquerda
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5,-0.5)

    # Direita
    glVertex3f(0.5,-0.5,-0.5)
    glVertex3f(0.5, 0.5,-0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5,-0.5, 0.5)

    # Topo
    glVertex3f(-0.5,0.5,-0.5)
    glVertex3f(-0.5,0.5, 0.5)
    glVertex3f( 0.5,0.5, 0.5)
    glVertex3f( 0.5,0.5,-0.5)

    # Base
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)

    glEnd()


# --------------------------------------------------
# Colisão AABB
# --------------------------------------------------

def colisao(x1, y1, z1,
            x2, y2, z2,
            tamanho=1.0):

    metade = tamanho / 2

    return (

        abs(x1 - x2) <= tamanho and
        abs(y1 - y2) <= tamanho and
        abs(z1 - z2) <= tamanho

    )


# --------------------------------------------------
# Inicialização do GLFW
# --------------------------------------------------

if not glfw.init():
    raise Exception("Erro ao iniciar GLFW")

janela = glfw.create_window(
    800,
    600,
    "Colisao AABB",
    None,
    None
)

if not janela:
    glfw.terminate()
    raise Exception("Erro ao criar janela")

glfw.make_context_current(janela)

glEnable(GL_DEPTH_TEST)

# --------------------------------------------------
# Compila os shaders
# --------------------------------------------------

vertex = carregar_shader("vertex_shader.glsl")
fragment = carregar_shader("fragment_shader.glsl")

program = compileProgram(
    compileShader(vertex, GL_VERTEX_SHADER),
    compileShader(fragment, GL_FRAGMENT_SHADER)
)

glUseProgram(program)

modelLoc = glGetUniformLocation(program, "model")
colorLoc = glGetUniformLocation(program, "color")

# --------------------------------------------------
# Posição dos cubos
# --------------------------------------------------

cubo1 = [-2.0, 0.0, -6.0]
cubo2 = [ 2.0, 0.0, -6.0]

wireframe = False
tecla_b = False

# --------------------------------------------------
# Loop principal
# --------------------------------------------------

while not glfw.window_should_close(janela):

    glfw.poll_events()

    # -----------------------------
    # Movimento do cubo 1
    # -----------------------------

    velocidade = 0.03

    if glfw.get_key(janela, glfw.KEY_LEFT) == glfw.PRESS:
        cubo1[0] -= velocidade

    if glfw.get_key(janela, glfw.KEY_RIGHT) == glfw.PRESS:
        cubo1[0] += velocidade

    if glfw.get_key(janela, glfw.KEY_UP) == glfw.PRESS:
        cubo1[2] += velocidade

    if glfw.get_key(janela, glfw.KEY_DOWN) == glfw.PRESS:
        cubo1[2] -= velocidade

    # -----------------------------
    # Alterna Wireframe (tecla B)
    # -----------------------------

    if glfw.get_key(janela, glfw.KEY_B) == glfw.PRESS:

        if not tecla_b:

            wireframe = not wireframe
            tecla_b = True

            if wireframe:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    else:
        tecla_b = False

    # -----------------------------
    # Teste de colisão
    # -----------------------------

    colidiu = colisao(
        cubo1[0], cubo1[1], cubo1[2],
        cubo2[0], cubo2[1], cubo2[2]
    )

    # -----------------------------
    # Recuo
    # -----------------------------

    if colidiu:

        if cubo1[0] < cubo2[0]:
            cubo1[0] -= velocidade
        else:
            cubo1[0] += velocidade

    # -----------------------------
    # Renderização
    # -----------------------------

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(
        45,
        800/600,
        0.1,
        100
    )

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # =============================
    # Cubo 1
    # =============================

    model = matriz_translacao(
        cubo1[0],
        cubo1[1],
        cubo1[2]
    )

    glUniformMatrix4fv(
        modelLoc,
        1,
        GL_FALSE,
        model
    )

    if colidiu:
        glUniform3f(colorLoc, 1.0, 0.0, 0.0)
    else:
        glUniform3f(colorLoc, 0.2, 0.7, 1.0)

    desenhar_cubo()

    # =============================
    # Cubo 2
    # =============================

    model = matriz_translacao(
        cubo2[0],
        cubo2[1],
        cubo2[2]
    )

    glUniformMatrix4fv(
        modelLoc,
        1,
        GL_FALSE,
        model
    )

    glUniform3f(
        colorLoc,
        0.2,
        1.0,
        0.2
    )

    desenhar_cubo()

    glfw.swap_buffers(janela)

glfw.terminate()