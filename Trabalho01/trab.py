import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# =========================
# VARIÁVEIS DO CARRO
# =========================
# Posição do carro no plano XZ
car_x = 0
car_z = 0

# Ângulo de rotação do carro
car_angle = 0

# Ângulo de rotação das rodas
wheel_rotation = 0

# Dicionário para armazenar as teclas pressionadas
keys = {}

# =========================
# CÂMERA TERCEIRA PESSOA
# =========================
cam_distance = 12
cam_height = 5

yaw = 0
pitch = -15

last_mouse_x = 960
last_mouse_y = 540

first_mouse = True

mouse_sensitivity = 0.2


# =========================
# CONFIGURAÇÃO OPENGL
# =========================
def init():
    # Define a cor do fundo (azul claro)
    glClearColor(0.6, 0.8, 1.0, 1.0)

    # Ativa o teste de profundidade para renderização 3D
    glEnable(GL_DEPTH_TEST)


# =========================
# RESIZE
# =========================
def resize(window, w, h):
    # Evita divisão por zero caso altura seja 0
    if h == 0:
        h = 1

    # Define a área visível da janela
    glViewport(0, 0, w, h)

    # Configura a matriz de projeção
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Define perspectiva da câmera
    gluPerspective(45.0, w / h, 0.1, 100.0)

    # Volta para matriz do modelo
    glMatrixMode(GL_MODELVIEW)


# =========================
# MOUSE
# =========================
def mouse_callback(window, xpos, ypos):

    global yaw, pitch
    global last_mouse_x, last_mouse_y
    global first_mouse

    if first_mouse:
        last_mouse_x = xpos
        last_mouse_y = ypos
        first_mouse = False

    xoffset = last_mouse_x - xpos
    yoffset = ypos - last_mouse_y

    last_mouse_x = xpos
    last_mouse_y = ypos

    xoffset *= mouse_sensitivity
    yoffset *= mouse_sensitivity

    yaw += xoffset
    pitch += yoffset

    if pitch > 45:
        pitch = 45

    if pitch < -45:
        pitch = -45


# =========================
# OBJ
# =========================
def load_obj(path):
    # Lista com todos os vértices do modelo
    vertices = []

    # Dicionário para separar os objetos do .obj
    # Ex: rodas, carroceria etc.
    objects = {}

    # Objeto atual sendo lido
    current_object = "default"

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:

            # Linha que define um novo objeto
            if line.startswith('o '):
                current_object = line.strip().split(maxsplit=1)[1]
                objects[current_object] = []

            # Linha de vértices
            elif line.startswith('v '):
                parts = line.strip().split()
                vertices.append(list(map(float, parts[1:4])))

            # Linha de faces
            elif line.startswith('f '):
                parts = line.strip().split()[1:]
                indices = []

                # Extrai os índices dos vértices
                for p in parts:
                    idx = p.split('/')[0]
                    indices.append(int(idx) - 1)

                # Triangulação da face
                # caso venha com mais de 3 vértices
                for i in range(1, len(indices) - 1):
                    face = [indices[0], indices[i], indices[i + 1]]

                    if current_object not in objects:
                        objects[current_object] = []

                    objects[current_object].append(face)

    return vertices, objects


# =========================
# CENTRO DO OBJETO
# =========================
def get_object_center(vertices, faces):
    # Lista com todos os pontos usados nas faces
    points = []

    for face in faces:
        for idx in face:
            points.append(vertices[idx])

    # Calcula a média dos pontos
    # para obter o centro do objeto
    x = sum(v[0] for v in points) / len(points)
    y = sum(v[1] for v in points) / len(points)
    z = sum(v[2] for v in points) / len(points)

    return x, y, z


# =========================
# DESENHO OBJ
# =========================
def draw_object(vertices, faces, gradient=False):

    # Desenha usando triângulos
    glBegin(GL_TRIANGLES)

    # Percorre cada face do objeto
    for face in faces:

        # Percorre os vértices da face
        for idx in face:

            # Coordenadas do vértice
            x, y, z = vertices[idx]

            # =========================
            # DEGRADÊ
            # =========================
            if gradient:

                # Normaliza altura do vértice
                # valor entre 0 e 1
                t = (y + 1.0) / 3.0
                t = max(0.0, min(1.0, t))

                # Parte inferior:
                # Roxo -> Vermelho
                if t < 0.5:

                    local_t = t / 0.5

                    r = 0.5 + (1.0 - 0.5) * local_t
                    g = 0.0
                    b = 0.5 + (0.0 - 0.5) * local_t

                # Parte superior:
                # Vermelho -> Azul
                else:

                    local_t = (t - 0.5) / 0.5

                    r = 1.0 + (0.0 - 1.0) * local_t
                    g = 0.0
                    b = 0.0 + (1.0 - 0.0) * local_t

                # Define cor do vértice
                glColor3f(r, g, b)

            # Desenha vértice
            glVertex3f(x, y, z)

    # Finaliza desenho
    glEnd()


# =========================
# MOVIMENTAÇÃO
# =========================
def update_movement():

    # Permite alterar variáveis globais
    global car_x, car_z
    global car_angle
    global wheel_rotation

    # Velocidade de movimento do carro
    speed = 0.15

    # Velocidade de rotação
    rot_speed = 2

    # =========================
    # ROTAÇÃO DO CARRO
    # =========================

    # Gira para esquerda
    if keys.get(glfw.KEY_A):
        car_angle += rot_speed

    # Gira para direita
    if keys.get(glfw.KEY_D):
        car_angle -= rot_speed

    # Converte ângulo para radianos
    rad = math.radians(car_angle)

    # =========================
    # MOVIMENTO PARA FRENTE
    # =========================
    if keys.get(glfw.KEY_W):

        # Move no eixo X usando seno
        car_x += math.sin(rad) * speed

        # Move no eixo Z usando cosseno
        car_z += math.cos(rad) * speed

        # Faz rodas girarem para frente
        wheel_rotation += 10

    # =========================
    # MOVIMENTO PARA TRÁS
    # =========================
    if keys.get(glfw.KEY_S):

        # Move para trás no eixo X
        car_x -= math.sin(rad) * speed

        # Move para trás no eixo Z
        car_z -= math.cos(rad) * speed

        # Faz rodas girarem para trás
        wheel_rotation -= 10


# =========================
# CHÃO
# =========================
def draw_ground():

    # Tamanho do chão
    size = 80

    # Inicia desenho de quadrilátero
    glBegin(GL_QUADS)

    # Canto inferior esquerdo
    glColor3f(0.2, 0.5, 0.2)
    glVertex3f(-size, 0, -size)

    # Canto superior esquerdo
    glColor3f(0.3, 0.7, 0.3)
    glVertex3f(-size, 0, size)

    # Canto superior direito
    glColor3f(0.4, 0.9, 0.4)
    glVertex3f(size, 0, size)

    # Canto inferior direito
    glColor3f(0.2, 0.6, 0.2)
    glVertex3f(size, 0, -size)

    # Finaliza desenho
    glEnd()


# =========================
# ESTRADA
# =========================
def draw_road():

    # Largura da estrada
    road_width = 6

    # Comprimento da estrada
    road_length = 80

    # Cor do asfalto
    glColor3f(0.2, 0.2, 0.2)

    # =========================
    # DESENHA ASFALTO
    # =========================
    glBegin(GL_QUADS)

    glVertex3f(-road_width, 0.01, -road_length)
    glVertex3f(-road_width, 0.01, road_length)
    glVertex3f(road_width, 0.01, road_length)
    glVertex3f(road_width, 0.01, -road_length)

    glEnd()

    # =========================
    # LINHAS AMARELAS
    # =========================

    # Cor das linhas
    glColor3f(1.0, 1.0, 0.0)

    # Começa no início da estrada
    z = -road_length

    # Cria várias linhas ao longo da estrada
    while z < road_length:

        glBegin(GL_QUADS)

        # Pequeno retângulo amarelo
        glVertex3f(-0.15, 0.02, z)
        glVertex3f(-0.15, 0.02, z + 2)

        glVertex3f(0.15, 0.02, z + 2)
        glVertex3f(0.15, 0.02, z)

        glEnd()

        # Espaçamento entre linhas
        z += 4


# =========================
# ÁRVORE
# =========================
def draw_tree():

    # =========================
    # TRONCO
    # =========================
    glColor3f(0.45, 0.25, 0.1)

    glBegin(GL_QUADS)

    # Frente
    glVertex3f(-0.2, 0, 0.2)
    glVertex3f(0.2, 0, 0.2)
    glVertex3f(0.2, 2, 0.2)
    glVertex3f(-0.2, 2, 0.2)

    # Trás
    glVertex3f(-0.2, 0, -0.2)
    glVertex3f(0.2, 0, -0.2)
    glVertex3f(0.2, 2, -0.2)
    glVertex3f(-0.2, 2, -0.2)

    # Esquerda
    glVertex3f(-0.2, 0, -0.2)
    glVertex3f(-0.2, 0, 0.2)
    glVertex3f(-0.2, 2, 0.2)
    glVertex3f(-0.2, 2, -0.2)

    # Direita
    glVertex3f(0.2, 0, -0.2)
    glVertex3f(0.2, 0, 0.2)
    glVertex3f(0.2, 2, 0.2)
    glVertex3f(0.2, 2, -0.2)

    # Topo
    glVertex3f(-0.2, 2, -0.2)
    glVertex3f(0.2, 2, -0.2)
    glVertex3f(0.2, 2, 0.2)
    glVertex3f(-0.2, 2, 0.2)

    # Base
    glVertex3f(-0.2, 0, -0.2)
    glVertex3f(0.2, 0, -0.2)
    glVertex3f(0.2, 0, 0.2)
    glVertex3f(-0.2, 0, 0.2)

    glEnd()

    # =========================
    # COPA
    # =========================
    glColor3f(0.0, 0.75, 0.0)

    glBegin(GL_TRIANGLES)

    # Frente
    glVertex3f(-1, 2, 1)
    glVertex3f(1, 2, 1)
    glVertex3f(0, 4, 0)

    # Direita
    glVertex3f(1, 2, 1)
    glVertex3f(1, 2, -1)
    glVertex3f(0, 4, 0)

    # Trás
    glVertex3f(1, 2, -1)
    glVertex3f(-1, 2, -1)
    glVertex3f(0, 4, 0)

    # Esquerda
    glVertex3f(-1, 2, -1)
    glVertex3f(-1, 2, 1)
    glVertex3f(0, 4, 0)

    glEnd()

    # =========================
    # BASE DA COPA
    # =========================
    glBegin(GL_QUADS)

    glVertex3f(-1, 2, 1)
    glVertex3f(1, 2, 1)
    glVertex3f(1, 2, -1)
    glVertex3f(-1, 2, -1)

    glEnd()


# =========================
# DISPLAY
# =========================
def display(vertices, objects):

    # Limpa buffer de cor e profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Reseta matriz atual
    glLoadIdentity()

    # =========================
    # CONFIGURAÇÃO DA CÂMERA
    # =========================

    # Converte ângulos para radianos
    rad_yaw = math.radians(yaw)
    rad_pitch = math.radians(pitch)

    # Calcula posição da câmera atrás do carro
    cam_x = car_x - math.sin(rad_yaw) * cam_distance
    cam_z = car_z - math.cos(rad_yaw) * cam_distance

    # Altura da câmera
    cam_y = cam_height + math.sin(rad_pitch) * 5

    # Define posição da câmera
    gluLookAt(
        cam_x, cam_y, cam_z,  # posição da câmera
        car_x, 2, car_z,      # ponto observado
        0, 1, 0               # vetor up
    )

    # =========================
    # DESENHA CENÁRIO
    # =========================

    # Desenha chão
    draw_ground()

    # Desenha estrada
    draw_road()

    # =========================
    # ÁRVORES ESQUERDA
    # =========================
    for z in range(-70, 80, 10):

        # Salva matriz atual
        glPushMatrix()

        # Move árvore
        glTranslatef(-10, 0, z)

        # Desenha árvore
        draw_tree()

        # Restaura matriz
        glPopMatrix()

    # =========================
    # ÁRVORES DIREITA
    # =========================
    for z in range(-70, 80, 10):

        glPushMatrix()

        glTranslatef(10, 0, z)

        draw_tree()

        glPopMatrix()

    # =========================
    # DESENHO DO CARRO
    # =========================
    glPushMatrix()

    # Move carro na cena
    glTranslatef(car_x, -1.05, car_z)

    # Rotaciona carro
    glRotatef(car_angle, 0, 1, 0)

    # Ajusta altura do modelo
    glTranslatef(0, 1, 0)

    # Percorre objetos do .obj
    for name, faces in objects.items():

        # =========================
        # RODAS
        # =========================
        if name in ["Roda_FL", "Roda_FR", "Roda_BL", "Roda_BR"]:

            # Cor das rodas
            glColor3f(0.1, 0.1, 0.1)

            # Obtém centro da roda
            cx, cy, cz = get_object_center(vertices, faces)

            glPushMatrix()

            # Move para centro da roda
            glTranslatef(cx, cy, cz)

            # Rotaciona roda
            glRotatef(wheel_rotation, 1, 0, 0)

            # Volta posição original
            glTranslatef(-cx, -cy, -cz)

            # Desenha roda
            draw_object(vertices, faces)

            glPopMatrix()

        # =========================
        # CARROCERIA
        # =========================
        else:

            # Desenha carro com degradê
            draw_object(vertices, faces, True)

    # Restaura matriz
    glPopMatrix()


# =========================
# TECLADO
# =========================
def key_callback(window, key, scancode, action, mods):

    # Quando tecla é pressionada
    if action == glfw.PRESS:
        keys[key] = True

    # Quando tecla é solta
    elif action == glfw.RELEASE:
        keys[key] = False

    # ESC fecha a janela
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

# =========================
# MAIN
# =========================
def main():

    # Inicializa a biblioteca GLFW
    if not glfw.init():
        return

    # =========================
    # CRIA JANELA
    # =========================
    window = glfw.create_window(
        1920,                  # largura
        1080,                  # altura
        "Cena 3D OpenGL",      # título da janela
        None,
        None
    )

    # Verifica se a janela foi criada
    if not window:
        glfw.terminate()
        return

    # Define contexto OpenGL atual
    glfw.make_context_current(window)

    # =========================
    # CALLBACKS
    # =========================

    # Callback de redimensionamento
    glfw.set_window_size_callback(window, resize)

    # Callback do teclado
    glfw.set_key_callback(window, key_callback)

    # Callback do mouse
    glfw.set_cursor_pos_callback(window, mouse_callback)

    # =========================
    # ESCONDE O CURSOR
    # =========================
    glfw.set_input_mode(
        window,
        glfw.CURSOR,
        glfw.CURSOR_DISABLED
    )

    # Obtém tamanho da janela
    width, height = glfw.get_framebuffer_size(window)

    # Ajusta viewport e projeção
    resize(window, width, height)

    # Inicializa configurações OpenGL
    init()

    # =========================
    # CARREGA MODELO .OBJ
    # =========================
    vertices, objects = load_obj("LowPolyFiatUNO.obj")

    # =========================
    # LOOP PRINCIPAL
    # =========================
    while not glfw.window_should_close(window):

        # Atualiza movimentação do carro
        update_movement()

        # Renderiza cena
        display(vertices, objects)

        # Troca buffers (double buffering)
        glfw.swap_buffers(window)

        # Processa eventos
        glfw.poll_events()

    # Finaliza GLFW
    glfw.terminate()


if __name__ == "__main__":
    main()