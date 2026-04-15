import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# =========================
# VARIÁVEIS DO CARRO
# =========================
car_x = 0
car_z = 0
car_angle = 0
wheel_rotation = 0

# estado das teclas
keys = {}


# =========================
# OPENGL SETUP
# =========================
def init():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)


def resize(window, w, h):
    if h == 0:
        h = 1

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, w / h, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


# =========================
# CARREGAR OBJ
# =========================
def load_obj(path):
    vertices = []
    faces = []

    with open(path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.strip().split()
                vertices.append([
                    float(parts[1]),
                    float(parts[2]),
                    float(parts[3])
                ])

            elif line.startswith('f '):
                parts = line.strip().split()[1:]
                face = []
                for p in parts:
                    idx = p.split('/')[0]
                    face.append(int(idx) - 1)
                faces.append(face)

    return vertices, faces


def draw_obj(vertices, faces):
    glBegin(GL_TRIANGLES)
    for face in faces:
        for idx in face:
            glVertex3f(*vertices[idx])
    glEnd()


# =========================
# EIXOS
# =========================
def draw_axes():
    glBegin(GL_LINES)

    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(10, 0, 0)

    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 10, 0)

    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 10)

    glEnd()


# =========================
# ATUALIZA MOVIMENTO (AQUI ESTÁ O SEGREDO)
# =========================
def update_movement():
    global car_x, car_z, car_angle, wheel_rotation

    speed = 0.2
    rot_speed = 2

    moving = False

    # rotação (permite junto com movimento)
    if keys.get(glfw.KEY_LEFT):
        car_angle += rot_speed
    if keys.get(glfw.KEY_RIGHT):
        car_angle -= rot_speed

    # direção atual
    rad = math.radians(car_angle)

    # movimento
    if keys.get(glfw.KEY_UP):
        car_x -= math.sin(rad) * speed
        car_z -= math.cos(rad) * speed
        wheel_rotation += 8
        moving = True

    if keys.get(glfw.KEY_DOWN):
        car_x += math.sin(rad) * speed
        car_z += math.cos(rad) * speed
        wheel_rotation -= 8
        moving = True


# =========================
# RENDER
# =========================
def display(carro_v, carro_f, roda_v, roda_f):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(8, 10, 20, 0, 0, 0, 0, 1, 0)

    glScalef(0.5, 0.5, 0.5)

    glPushMatrix()

    glTranslatef(car_x, 0, car_z)
    glRotatef(car_angle, 0, 1, 0)

    # carro
    glPushMatrix()
    glTranslatef(0, 1, 0)
    glColor3f(0.1, 0.3, 1.0)
    draw_obj(carro_v, carro_f)
    glPopMatrix()

    # rodas
    posicoes = [
        (1.2, 1, 3),
        (-1.2, 1, 3),
        (1.2, 1, -3),
        (-1.2, 1, -3)
    ]

    for x, y, z in posicoes:
        glPushMatrix()
        glTranslatef(x, y, z)
        glRotatef(wheel_rotation, 1, 0, 0)
        glColor3f(1, 0.2, 0.2)
        draw_obj(roda_v, roda_f)
        glPopMatrix()

    glPopMatrix()

    draw_axes()


# =========================
# TECLADO (AGORA SÓ REGISTRA ESTADO)
# =========================
def key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False


# =========================
# MAIN
# =========================
def main():
    if not glfw.init():
        return

    window = glfw.create_window(1280, 720, "Carro 3D", None, None)
    glfw.make_context_current(window)

    glfw.set_window_size_callback(window, resize)
    glfw.set_key_callback(window, key_callback)

    init()

    carro_v, carro_f = load_obj("carro.obj")
    roda_v, roda_f = load_obj("roda2.obj")

    while not glfw.window_should_close(window):

        update_movement()  # <<< AQUI FAZ CURVA SUAVE

        display(carro_v, carro_f, roda_v, roda_f)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()