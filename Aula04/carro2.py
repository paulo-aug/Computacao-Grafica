import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# =========================
# VARIÁVEIS GLOBAIS
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
# CONFIGURAÇÃO INICIAL OPENGL
# =========================
def init():
    # Define a cor do fundo (azul claro)
    glClearColor(0.6, 0.8, 1.0, 1.0)

    # Ativa o teste de profundidade para renderização 3D
    glEnable(GL_DEPTH_TEST)


# =========================
# AJUSTE DA JANELA
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
# LEITURA DO OBJ
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
# DESENHO DO OBJETO
# =========================
def draw_object(vertices, faces):
    glBegin(GL_TRIANGLES)

    # Desenha cada triângulo
    for face in faces:
        for idx in face:
            glVertex3f(*vertices[idx])

    glEnd()


# =========================
# MOVIMENTAÇÃO
# =========================
def update_movement():
    global car_x, car_z, car_angle, wheel_rotation

    # Velocidade de movimento
    speed = 0.1

    # Velocidade de rotação do carro
    rot_speed = 2

    # Rotação para esquerda
    if keys.get(glfw.KEY_LEFT):
        car_angle += rot_speed

    # Rotação para direita
    if keys.get(glfw.KEY_RIGHT):
        car_angle -= rot_speed

    # Converte ângulo para radianos
    rad = math.radians(car_angle)

    # Movimento para frente
    if keys.get(glfw.KEY_UP):
        car_x += math.sin(rad) * speed
        car_z += math.cos(rad) * speed

        # Faz a roda girar para frente
        wheel_rotation += 10

    # Movimento para trás
    if keys.get(glfw.KEY_DOWN):
        car_x -= math.sin(rad) * speed
        car_z -= math.cos(rad) * speed

        # Faz a roda girar para trás
        wheel_rotation -= 10


# =========================
# RENDERIZAÇÃO DA CENA
# =========================
def display(vertices, objects):
    # Limpa tela e profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Define posição da câmera
    gluLookAt(8, 10, 20, 0, 0, 0, 0, 1, 0)

    glPushMatrix()

    # Move o carro no cenário
    glTranslatef(car_x, 0, car_z)

    # Rotaciona o carro
    glRotatef(car_angle, 0, 1, 0)

    # Ajusta altura do modelo
    glTranslatef(0, 1, 0)

    # Percorre cada objeto do .obj
    for name, faces in objects.items():

        # Se for uma roda
        if name in ["Roda_FL", "Roda_FR", "Roda_BL", "Roda_BR"]:
            # Cor cinza escuro
            glColor3f(0.15, 0.15, 0.15)

            # Centro da roda
            cx, cy, cz = get_object_center(vertices, faces)

            glPushMatrix()

            # Move para o centro da roda
            glTranslatef(cx, cy, cz)

            # Rotaciona a roda no próprio eixo
            glRotatef(wheel_rotation, 1, 0, 0)

            # Volta para posição original
            glTranslatef(-cx, -cy, -cz)

            # Desenha roda
            draw_object(vertices, faces)

            glPopMatrix()

        else:
            # Carroceria vermelha
            glColor3f(0.9, 0.2, 0.2)

            # Desenha carro
            draw_object(vertices, faces)

    glPopMatrix()


# =========================
# LEITURA DO TECLADO
# =========================
def key_callback(window, key, scancode, action, mods):
    # Quando tecla é pressionada
    if action == glfw.PRESS:
        keys[key] = True

    # Quando tecla é solta
    elif action == glfw.RELEASE:
        keys[key] = False


# =========================
# FUNÇÃO PRINCIPAL
# =========================
def main():
    # Inicializa GLFW
    if not glfw.init():
        return

    # Cria janela
    window = glfw.create_window(1280, 720, "Carro 3D", None, None)

    if not window:
        glfw.terminate()
        return

    # Torna janela contexto atual
    glfw.make_context_current(window)

    # Callbacks
    glfw.set_window_size_callback(window, resize)
    glfw.set_key_callback(window, key_callback)

    # Configura OpenGL
    init()

    # Carrega modelo
    vertices, objects = load_obj("LowPolyFiatUNO.obj")

    # Loop principal
    while not glfw.window_should_close(window):
        update_movement()
        display(vertices, objects)

        glfw.swap_buffers(window)
        glfw.poll_events()

    # Finaliza GLFW
    glfw.terminate()


if __name__ == "__main__":
    main()