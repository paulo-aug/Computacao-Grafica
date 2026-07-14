import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image


def carregar_textura(caminho):

    imagem = Image.open(caminho)
    imagem = imagem.transpose(Image.FLIP_TOP_BOTTOM)
    imagem = imagem.convert("RGB")

    largura, altura = imagem.size
    dados = imagem.tobytes()

    textura = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura)

    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGB,
        largura,
        altura,
        0,
        GL_RGB,
        GL_UNSIGNED_BYTE,
        dados
    )

    # Gera automaticamente os mipmaps
    glGenerateMipmap(GL_TEXTURE_2D)

    # Filtros
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                    GL_LINEAR_MIPMAP_LINEAR)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                    GL_LINEAR)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    return textura


def desenhar_cubo():

    glBegin(GL_QUADS)

    # Frente
    glTexCoord2f(0,0); glVertex3f(-1,-1, 1)
    glTexCoord2f(1,0); glVertex3f( 1,-1, 1)
    glTexCoord2f(1,1); glVertex3f( 1, 1, 1)
    glTexCoord2f(0,1); glVertex3f(-1, 1, 1)

    # Trás
    glTexCoord2f(0,0); glVertex3f( 1,-1,-1)
    glTexCoord2f(1,0); glVertex3f(-1,-1,-1)
    glTexCoord2f(1,1); glVertex3f(-1, 1,-1)
    glTexCoord2f(0,1); glVertex3f( 1, 1,-1)

    # Esquerda
    glTexCoord2f(0,0); glVertex3f(-1,-1,-1)
    glTexCoord2f(1,0); glVertex3f(-1,-1, 1)
    glTexCoord2f(1,1); glVertex3f(-1, 1, 1)
    glTexCoord2f(0,1); glVertex3f(-1, 1,-1)

    # Direita
    glTexCoord2f(0,0); glVertex3f(1,-1, 1)
    glTexCoord2f(1,0); glVertex3f(1,-1,-1)
    glTexCoord2f(1,1); glVertex3f(1, 1,-1)
    glTexCoord2f(0,1); glVertex3f(1, 1, 1)

    # Topo
    glTexCoord2f(0,0); glVertex3f(-1,1, 1)
    glTexCoord2f(1,0); glVertex3f( 1,1, 1)
    glTexCoord2f(1,1); glVertex3f( 1,1,-1)
    glTexCoord2f(0,1); glVertex3f(-1,1,-1)

    # Base
    glTexCoord2f(0,0); glVertex3f(-1,-1,-1)
    glTexCoord2f(1,0); glVertex3f( 1,-1,-1)
    glTexCoord2f(1,1); glVertex3f( 1,-1, 1)
    glTexCoord2f(0,1); glVertex3f(-1,-1, 1)

    glEnd()


if not glfw.init():
    raise Exception("Erro ao iniciar GLFW")

janela = glfw.create_window(800, 600, "Exercício 2", None, None)

if not janela:
    glfw.terminate()
    raise Exception("Erro ao criar janela")

glfw.make_context_current(janela)

glEnable(GL_DEPTH_TEST)
glEnable(GL_TEXTURE_2D)

textura = carregar_textura("textura.jpg")

distancia = -6.0
angulo = 0

while not glfw.window_should_close(janela):

    glfw.poll_events()

    # Aproxima
    if glfw.get_key(janela, glfw.KEY_W) == glfw.PRESS:
        distancia += 0.05

    # Afasta
    if glfw.get_key(janela, glfw.KEY_S) == glfw.PRESS:
        distancia -= 0.05

    angulo += 0.4

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800/600, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(0, 0, distancia)

    glRotatef(angulo, 1, 1, 0)

    glBindTexture(GL_TEXTURE_2D, textura)

    desenhar_cubo()

    glfw.swap_buffers(janela)

glfw.terminate()