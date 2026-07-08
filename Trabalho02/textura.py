import pygame

from OpenGL.GL import *
from OpenGL.GLU import *


def carregar_textura(caminho):
    """
    Carrega uma textura utilizando o Pygame
    e cria uma textura no OpenGL.
    """

    imagem = pygame.image.load(caminho)

    imagem = pygame.transform.flip(imagem, False, True)

    largura = imagem.get_width()
    altura = imagem.get_height()

    dados = pygame.image.tostring(imagem, "RGBA", True)

    textura = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, textura)

    # Filtros
    glTexParameteri(
        GL_TEXTURE_2D,
        GL_TEXTURE_MIN_FILTER,
        GL_LINEAR_MIPMAP_LINEAR
    )

    glTexParameteri(
        GL_TEXTURE_2D,
        GL_TEXTURE_MAG_FILTER,
        GL_LINEAR
    )

    # Repete textura caso necessário
    glTexParameteri(
        GL_TEXTURE_2D,
        GL_TEXTURE_WRAP_S,
        GL_REPEAT
    )

    glTexParameteri(
        GL_TEXTURE_2D,
        GL_TEXTURE_WRAP_T,
        GL_REPEAT
    )

    # Cria mipmaps
    gluBuild2DMipmaps(
        GL_TEXTURE_2D,
        GL_RGBA,
        largura,
        altura,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        dados
    )

    glBindTexture(GL_TEXTURE_2D, 0)

    return textura


def desenhar_fundo(textura):
    """
    Desenha um plano de fundo com textura.
    """

    # Fundo não recebe iluminação
    glDisable(GL_LIGHTING)

    glEnable(GL_TEXTURE_2D)

    glBindTexture(GL_TEXTURE_2D, textura)

    glPushMatrix()

    # Coloca o fundo atrás de todos os objetos
    glTranslatef(0, 0, -5)

    tamanho = 18

    glColor3f(1, 1, 1)

    glBegin(GL_QUADS)

    glTexCoord2f(0, 0)
    glVertex3f(-tamanho, -tamanho, 0)

    glTexCoord2f(1, 0)
    glVertex3f(tamanho, -tamanho, 0)

    glTexCoord2f(1, 1)
    glVertex3f(tamanho, tamanho, 0)

    glTexCoord2f(0, 1)
    glVertex3f(-tamanho, tamanho, 0)

    glEnd()

    glPopMatrix()

    glBindTexture(GL_TEXTURE_2D, 0)

    glDisable(GL_TEXTURE_2D)

    glEnable(GL_LIGHTING)