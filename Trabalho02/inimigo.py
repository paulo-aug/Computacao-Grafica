import math
import random

from OpenGL.GL import *


class Inimigo:

    def __init__(self):

        # Nasce nas bordas do cenário
        lado = random.choice([
            "cima",
            "baixo",
            "esquerda",
            "direita"
        ])


        if lado == "cima":

            self.x = random.uniform(-13, 13)
            self.y = 13


        elif lado == "baixo":

            self.x = random.uniform(-13, 13)
            self.y = -13


        elif lado == "esquerda":

            self.x = -13
            self.y = random.uniform(-13, 13)


        elif lado == "direita":

            self.x = 13
            self.y = random.uniform(-13, 13)

        # Direção aleatória
        angulo = random.uniform(0, 360)
        rad = math.radians(angulo)

        # Velocidade
        velocidade = random.uniform(1.5, 3.5)

        self.vx = math.cos(rad) * velocidade
        self.vy = math.sin(rad) * velocidade

        # Rotação visual
        self.rotacao = 0
        self.vel_rotacao = random.uniform(-50, 50)

        # Escala do asteroide
        self.escala = 0.7

        # Raio para colisão
        self.raio = 0.8 * self.escala

        # Cores aleatorias
        self.cor = (
            random.uniform(0.4, 0.5),
            random.uniform(0.4, 0.5),
            random.uniform(0.4, 0.5)
        )

    def atualizar(self, delta):

        self.x += self.vx * delta
        self.y += self.vy * delta

        self.rotacao += self.vel_rotacao * delta

        limite = 13

        # Teletransporte nas bordas
        if self.x > limite:
            self.x = -limite

        elif self.x < -limite:
            self.x = limite

        if self.y > limite:
            self.y = -limite

        elif self.y < -limite:
            self.y = limite

    def desenhar(self):

        glPushMatrix()

        glTranslatef(self.x, self.y, 0)
        glRotatef(self.rotacao, 0, 0, 1)
        glScalef(self.escala, self.escala, 1.0)

        # Cor do asteroide
        glColor3f(*self.cor)

        # Asteroide com formato irregular
        vertices = [
            (0.9, 0.0),
            (0.6, 0.6),
            (0.0, 0.9),
            (-0.7, 0.5),
            (-0.9, 0.0),
            (-0.5, -0.7),
            (0.0, -0.9),
            (0.7, -0.5),
        ]

        glBegin(GL_POLYGON)

        # Normal da superfície para iluminação
        glNormal3f(0.0, 0.0, 1.0)

        for vx, vy in vertices:
            glVertex3f(vx, vy, 0.0)

        glEnd()

        # Contorno sem iluminação
        glDisable(GL_LIGHTING)

        glColor3f(1.0, 1.0, 1.0)

        glBegin(GL_LINE_LOOP)

        for vx, vy in vertices:
            glVertex3f(vx, vy, 0.0)

        glEnd()

        glEnable(GL_LIGHTING)

        glPopMatrix()