import math
import pygame

from OpenGL.GL import *


class Nave:

    def __init__(self):

        # Posição da nave
        self.x = 0.0
        self.y = 0.0

        # Velocidade
        self.vx = 0.0
        self.vy = 0.0

        # Rotação (graus)
        self.angulo = 90.0

        # Configurações
        self.aceleracao = 15.0
        self.rotacao_vel = 180.0
        self.atrito = 0.99
        self.velocidade_max = 12.0

        # Raio utilizado na colisão
        self.raio = 0.7

        self.acelerando = False

    def atualizar(self, delta):

        teclas = pygame.key.get_pressed()

        self.acelerando = False

        # Rotação
        if teclas[pygame.K_a]:
            self.acelerando = True
            self.angulo += self.rotacao_vel * delta

        if teclas[pygame.K_d]:
            self.acelerando = True
            self.angulo -= self.rotacao_vel * delta

        # Empuxo
        if teclas[pygame.K_w]:

            self.acelerando = True

            rad = math.radians(self.angulo)

            self.vx += math.cos(rad) * self.aceleracao * delta
            self.vy += math.sin(rad) * self.aceleracao * delta

        # Limita velocidade máxima
        velocidade = math.sqrt(self.vx ** 2 + self.vy ** 2)

        if velocidade > self.velocidade_max:

            fator = self.velocidade_max / velocidade

            self.vx *= fator
            self.vy *= fator

        # Atualiza posição
        self.x += self.vx * delta
        self.y += self.vy * delta

        # Atrito
        self.vx *= self.atrito
        self.vy *= self.atrito

        # Teletransporte
        limite = 12

        if self.x > limite:
            self.x = -limite

        if self.x < -limite:
            self.x = limite

        if self.y > limite:
            self.y = -limite

        if self.y < -limite:
            self.y = limite

    def desenhar(self, textura):

        glPushMatrix()

        glTranslatef(self.x, self.y, 0)
        glRotatef(self.angulo - 90, 0, 0, 1)

        if self.acelerando:

            glDisable(GL_LIGHTING)

            glBegin(GL_TRIANGLES)

            # Chama externa (laranja)
            glColor3f(1.0, 0.5, 0.0)

            glVertex3f(-0.20, -0.45, 0.0)
            glVertex3f(0.20, -0.45, 0.0)
            glVertex3f(0.0, -1.15, 0.0)

            glEnd()

            glBegin(GL_TRIANGLES)

            # Chama interna (amarela)
            glColor3f(1.0, 1.0, 0.0)

            glVertex3f(-0.10, -0.45, 0.0)
            glVertex3f(0.10, -0.45, 0.0)
            glVertex3f(0.0, -0.90, 0.0)

            glEnd()

            glEnable(GL_LIGHTING)

        # Habilita textura
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textura)

        glColor3f(1.0, 1.0, 1.0)

        glBegin(GL_TRIANGLES)

        glNormal3f(0.0, 0.0, 1.0)

        # Ponta da nave
        glTexCoord2f(0.5, 1.0)
        glVertex3f(0.0, 0.8, 0.0)

        # Canto esquerdo
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5, -0.5, 0.0)

        # Canto direito
        glTexCoord2f(1.0, 0.0)
        glVertex3f(0.5, -0.5, 0.0)

        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)

        glPopMatrix()