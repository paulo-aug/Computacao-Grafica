import glfw
from OpenGL.GL import *

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Coelho", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        # Corpo
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(-0.3, -0.3)
        glVertex2f(0.3, -0.3)
        glVertex2f(0.0, 0.2)
        glEnd()

        # Cabeca
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(-0.2, 0.2)
        glVertex2f(0.2, 0.2)
        glVertex2f(0.0, 0.6)
        glEnd()

        # Orelha esquerda
        glColor3f(1.0, 0.8, 0.9)
        glBegin(GL_TRIANGLES)
        glVertex2f(-0.15, 0.4)
        glVertex2f(-0.05, 0.6)
        glVertex2f(-0.2, 0.9)
        glEnd()

        # Orelha direita
        glColor3f(1.0, 0.8, 0.9)
        glBegin(GL_TRIANGLES)
        glVertex2f(0.05, 0.6)
        glVertex2f(0.15, 0.4)
        glVertex2f(0.2, 0.9)
        glEnd()

        # Olho esquerdo (quadrado preto)
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_QUADS)
        glVertex2f(-0.12, 0.35)
        glVertex2f(-0.08, 0.35)
        glVertex2f(-0.08, 0.39)
        glVertex2f(-0.12, 0.39)
        glEnd()

        # Olho direito (quadrado preto)
        glBegin(GL_QUADS)
        glVertex2f(0.08, 0.35)
        glVertex2f(0.12, 0.35)
        glVertex2f(0.12, 0.39)
        glVertex2f(0.08, 0.39)
        glEnd()

        # Nariz (triângulo rosa)
        glColor3f(1.0, 0.6, 0.7)
        glBegin(GL_TRIANGLES)
        glVertex2f(-0.03, 0.3)
        glVertex2f(0.03, 0.3)
        glVertex2f(0.0, 0.27)
        glEnd()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

main()


