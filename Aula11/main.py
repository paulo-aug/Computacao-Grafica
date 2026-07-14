import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math


# -----------------------------
# Desenha um quadrado
# -----------------------------
def desenhar_quadrado(x, y, tamanho, cor):

    glColor3f(cor[0], cor[1], cor[2])

    metade = tamanho / 2

    glBegin(GL_QUADS)

    glVertex2f(x - metade, y - metade)
    glVertex2f(x + metade, y - metade)
    glVertex2f(x + metade, y + metade)
    glVertex2f(x - metade, y + metade)

    glEnd()


# -----------------------------
# Desenha uma circunferência
# -----------------------------
def desenhar_circulo(x, y, raio, cor):

    glColor3f(cor[0], cor[1], cor[2])

    glBegin(GL_LINE_LOOP)

    for i in range(100):

        ang = 2 * math.pi * i / 100

        glVertex2f(
            x + math.cos(ang) * raio,
            y + math.sin(ang) * raio
        )

    glEnd()


# -----------------------------
# Bounding Sphere
# -----------------------------
def distancia(x1, y1, x2, y2):

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )


# -----------------------------
# Detecta o estado da Esfera
# -----------------------------
def estado_esfera(x1, y1, r, x2, y2):

    d = distancia(x1, y1, x2, y2)

    if d <= r:
        return "COLISAO"

    elif d <= r * 1.5:
        return "AVISO"

    else:
        return "LIVRE"


# -----------------------------
# Colisão AABB
# -----------------------------
def colisao_aabb(x1, y1, t1,
                 x2, y2, t2):

    metade1 = t1 / 2
    metade2 = t2 / 2

    return (

        abs(x1 - x2) <= metade1 + metade2 and
        abs(y1 - y2) <= metade1 + metade2

    )


# -----------------------------
# Direção da colisão
# -----------------------------
def direcao_colisao(x1, y1,
                    x2, y2):

    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) > abs(dy):

        if dx > 0:
            return "DIREITA"

        else:
            return "ESQUERDA"

    else:

        if dy > 0:
            return "CIMA"

        else:
            return "BAIXO"
        


# -----------------------------
# Inicialização do GLFW
# -----------------------------
if not glfw.init():
    raise Exception("Erro ao iniciar GLFW")

janela = glfw.create_window(
    800,
    600,
    "Bounding Sphere + AABB",
    None,
    None
)

if not janela:
    glfw.terminate()
    raise Exception("Erro ao criar janela")

glfw.make_context_current(janela)

# -----------------------------
# Objetos
# -----------------------------
obj1_x = -0.5
obj1_y = 0.0

obj2_x = 0.5
obj2_y = 0.0

tamanho = 0.25
raio = 0.30

# -----------------------------
# Loop principal
# -----------------------------
while not glfw.window_should_close(janela):

    glfw.poll_events()

    velocidade = 0.01

    # Movimento do objeto principal
    if glfw.get_key(janela, glfw.KEY_LEFT) == glfw.PRESS:
        obj1_x -= velocidade

    if glfw.get_key(janela, glfw.KEY_RIGHT) == glfw.PRESS:
        obj1_x += velocidade

    if glfw.get_key(janela, glfw.KEY_UP) == glfw.PRESS:
        obj1_y += velocidade

    if glfw.get_key(janela, glfw.KEY_DOWN) == glfw.PRESS:
        obj1_y -= velocidade

    # -----------------------------
    # Bounding Sphere
    # -----------------------------
    estado = estado_esfera(
        obj1_x,
        obj1_y,
        raio,
        obj2_x,
        obj2_y
    )

    if estado == "LIVRE":
        cor1 = (0.0, 0.4, 1.0)

    elif estado == "AVISO":
        cor1 = (1.0, 1.0, 0.0)

    else:
        cor1 = (1.0, 0.0, 0.0)

    # -----------------------------
    # Exercício 2
    # AABB
    # -----------------------------
    cor2 = (0.0, 1.0, 0.0)

    if colisao_aabb(
        obj1_x,
        obj1_y,
        tamanho,
        obj2_x,
        obj2_y,
        tamanho
    ):

        lado = direcao_colisao(
            obj1_x,
            obj1_y,
            obj2_x,
            obj2_y
        )

        if lado == "ESQUERDA":
            cor2 = (1.0, 0.0, 0.0)

        elif lado == "DIREITA":
            cor2 = (0.0, 1.0, 0.0)

        elif lado == "CIMA":
            cor2 = (0.0, 0.0, 1.0)

        elif lado == "BAIXO":
            cor2 = (1.0, 1.0, 0.0)

    # -----------------------------
    # Renderização
    # -----------------------------
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Esfera externa (1.5R)
    desenhar_circulo(
        obj1_x,
        obj1_y,
        raio * 1.5,
        (1.0, 1.0, 1.0)
    )

    # Esfera interna (R)
    desenhar_circulo(
        obj1_x,
        obj1_y,
        raio,
        (0.0, 1.0, 1.0)
    )

    # Objeto principal
    desenhar_quadrado(
        obj1_x,
        obj1_y,
        tamanho,
        cor1
    )

    # Segundo objeto
    desenhar_quadrado(
        obj2_x,
        obj2_y,
        tamanho,
        cor2
    )

    glfw.swap_buffers(janela)

glfw.terminate()