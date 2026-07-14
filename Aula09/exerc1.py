import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image


# Carrega a textura
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

    # Filtro
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Repetição da textura
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    return textura


# Desenha um quadrado
def desenhar_quadrado():

    glBegin(GL_QUADS)

    # UV (0,0)
    glTexCoord2f(0.0, 0.0)
    glVertex2f(-0.8, -0.8)

    # UV (3,0)
    glTexCoord2f(3.0, 0.0)
    glVertex2f(0.8, -0.8)

    # UV (3,3)
    glTexCoord2f(3.0, 3.0)
    glVertex2f(0.8, 0.8)

    # UV (0,3)
    glTexCoord2f(0.0, 3.0)
    glVertex2f(-0.8, 0.8)

    glEnd()


# Inicializa GLFW
if not glfw.init():
    raise Exception("Erro ao iniciar GLFW")

janela = glfw.create_window(
    800,
    600,
    "Exercicio 1 - GL_REPEAT",
    None,
    None
)

if not janela:
    glfw.terminate()
    raise Exception("Erro ao criar janela")

glfw.make_context_current(janela)

# Ativa texturas
glEnable(GL_TEXTURE_2D)

# Carrega textura
textura = carregar_textura("textura.jpg")

while not glfw.window_should_close(janela):

    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()

    glBindTexture(GL_TEXTURE_2D, textura)

    desenhar_quadrado()

    glfw.swap_buffers(janela)

glfw.terminate()