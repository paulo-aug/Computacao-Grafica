import glfw
from OpenGL.GL import *
import math

# Função para desenhar círculos com cores e transparência
def desenha_circulo(cx, cy, rx, ry, cor_r, cor_g, cor_b, cor_a=1.0, segmentos=64):
    glColor4f(cor_r, cor_g, cor_b, cor_a)
    glBegin(GL_POLYGON)
    for i in range(segmentos):
        angulo = 2.0 * math.pi * i / segmentos
        x = cx + math.cos(angulo) * rx
        y = cy + math.sin(angulo) * ry
        glVertex2f(x, y)
    glEnd()

def main():
    if not glfw.init(): 
        return

    janela = glfw.create_window(800, 800, "Ovo de Páscoa", None, None)
    glfw.make_context_current(janela)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    while not glfw.window_should_close(janela):
        # Cor de fundo cinza claro
        glClearColor(0.95, 0.95, 0.95, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Sombra do ovo (preto translúcido)
        desenha_circulo(0.03, -0.03, 0.4, 0.5, 0.0, 0.0, 0.0, 0.3)

        # Ovo principal (lilás)
        desenha_circulo(0.0, 0.0, 0.4, 0.5, 0.7, 0.5, 1.0)

        # Brilho (roxo)
        desenha_circulo(-0.15, 0.25, 0.12, 0.12, 0.6, 0.4, 0.8)

        # Bolinhas brancas
        desenha_circulo(-0.2, -0.25, 0.03, 0.03, 1.0, 1.0, 1.0)
        desenha_circulo(0.0, -0.35, 0.03, 0.03, 1.0, 1.0, 1.0)
        desenha_circulo(0.2, -0.25, 0.03, 0.03, 1.0, 1.0, 1.0)

        # Onda laranja
        glLineWidth(3)
        glBegin(GL_LINE_STRIP)
        glColor3f(1.0, 0.7, 0.3)
        for x in [i/100 for i in range(-32, 33)]:
            y = 0.05 + 0.03 * math.sin(x * 15)
            glVertex2f(x, y)
        glEnd()

        # Onda rosa
        glBegin(GL_LINE_STRIP)
        glColor3f(1.0, 0.5, 0.8)
        for x in [i/100 for i in range(-32, 33)]:
            y = -0.05 + 0.03 * math.sin(x * 15)
            glVertex2f(x, y)
        glEnd()

        glfw.swap_buffers(janela)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()