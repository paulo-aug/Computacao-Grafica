import math

from OpenGL.GL import *


class Projetil:

    def __init__(self, x, y, angulo):

        # Posição inicial
        self.x = x
        self.y = y

        # Ângulo da nave no momento do disparo
        self.angulo = angulo

        # Velocidade do projétil
        self.velocidade = 20.0

        # Raio para colisão
        self.raio = 0.15

        # Tempo de vida (segundos)
        self.tempo_vida = 2.5

        # Calcula direção
        rad = math.radians(angulo)

        self.vx = math.cos(rad) * self.velocidade
        self.vy = math.sin(rad) * self.velocidade

    def atualizar(self, delta):

        self.x += self.vx * delta
        self.y += self.vy * delta

        self.tempo_vida -= delta

    def desenhar(self):

        glPushMatrix()

        glTranslatef(self.x, self.y, 0)

        # Cor do projétil
        glColor3f(1.0, 1.0, 0.0)

        raio = 0.10

        glBegin(GL_POLYGON)

        # Normal da superfície (necessária para iluminação)
        glNormal3f(0.0, 0.0, 1.0)

        for i in range(20):

            ang = 2 * math.pi * i / 20

            glVertex3f(
                math.cos(ang) * raio,
                math.sin(ang) * raio,
                0.0
            )

        glEnd()

        glPopMatrix()

    def esta_vivo(self):

        limite = 13

        if self.tempo_vida <= 0:
            return False

        if self.x > limite:
            return False

        if self.x < -limite:
            return False

        if self.y > limite:
            return False

        if self.y < -limite:
            return False

        return True