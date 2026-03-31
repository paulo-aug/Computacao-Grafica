import glfw
from OpenGL.GL import *

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Chocolate Diagonal", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        # Cor de fundo cinza claro
        glClearColor(0.95, 0.95, 0.95, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glLoadIdentity()

        # Rotaciona 30 graus (diagonal)
        glRotatef(30, 0, 0, 1)

        # Barra principal
        glColor3f(0.4, 0.2, 0.1)
        glBegin(GL_QUADS)
        glVertex2f(-0.6, -0.4)
        glVertex2f(0.6, -0.4)
        glVertex2f(0.6, 0.4)
        glVertex2f(-0.6, 0.4)
        glEnd()

        # Gomos
        glColor3f(0.3, 0.15, 0.05)
        rows = 3
        cols = 4

        width = 1.2 / cols
        height = 0.8 / rows

        start_x = -0.6
        start_y = -0.4

        for i in range(rows):
            for j in range(cols):
                x = start_x + j * width
                y = start_y + i * height

                glBegin(GL_QUADS)
                glVertex2f(x + 0.02, y + 0.02)
                glVertex2f(x + width - 0.02, y + 0.02)
                glVertex2f(x + width - 0.02, y + height - 0.02)
                glVertex2f(x + 0.02, y + height - 0.02)
                glEnd()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

main()