import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from nave import Nave
from projetil import Projetil
from inimigo import Inimigo
from collision import verificar_colisoes
from textura import carregar_textura, desenhar_fundo

# -----------------------------
# Configurações da janela
# -----------------------------
LARGURA = 1000
ALTURA = 700
FPS = 60

# Objetos do jogo
nave = Nave()
projeteis = []

# Inimigos
inimigos = []

# Pontuação
score = 0

game_over = False

# Fonte
fonte = None

textura_fundo = None
textura_nave = None

# Cria alguns inimigos
for _ in range(6):
    inimigos.append(Inimigo())


def desenhar_texto(texto, x, y):

    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)

    glEnable(GL_BLEND)
    glBlendFunc(
        GL_SRC_ALPHA,
        GL_ONE_MINUS_SRC_ALPHA
    )

    superficie = fonte.render(
        texto,
        True,
        (255, 255, 255)
    )

    largura = superficie.get_width()
    altura = superficie.get_height()

    dados = pygame.image.tostring(
        superficie,
        "RGBA",
        True
    )

    glWindowPos2d(
        x,
        ALTURA - y - altura
    )

    glDrawPixels(
        largura,
        altura,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        dados
    )

    glDisable(GL_BLEND)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)


def tela_game_over():

    glClear(
        GL_COLOR_BUFFER_BIT |
        GL_DEPTH_BUFFER_BIT
    )

    glLoadIdentity()

    glDisable(GL_LIGHTING)

    desenhar_texto(
        "GAME OVER",
        420,
        280
    )

    desenhar_texto(
        f"Score: {score}",
        450,
        330
    )

    desenhar_texto(
        "ENTER - Jogar novamente",
        350,
        380
    )

    desenhar_texto(
        "ESC - Sair",
        430,
        430
    )

    pygame.display.flip()


def reiniciar_jogo():

    global score
    global game_over

    score = 0
    game_over = False

    nave.x = 0
    nave.y = 0

    nave.vx = 0
    nave.vy = 0

    projeteis.clear()

    inimigos.clear()

    for _ in range(6):
        inimigos.append(Inimigo())


def inicializar():

    global fonte

    pygame.init()

    pygame.display.set_mode(
        (LARGURA, ALTURA),
        DOUBLEBUF | OPENGL
    )

    pygame.display.set_caption("Asteroids - Computação Gráfica")

    fonte = pygame.font.SysFont("Arial", 24)

    global textura_fundo
    global textura_nave

    textura_fundo = carregar_textura("assets/space.png")
    textura_nave = carregar_textura("assets/nave.jpg")

    glClearColor(0.02, 0.02, 0.05, 1)

    # ----------------------------
    # OpenGL
    # ----------------------------
    glEnable(GL_DEPTH_TEST)

    # ----------------------------
    # Iluminação
    # ----------------------------
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Permite usar glColor3f() como material
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    # Luz ambiente
    glLightfv(GL_LIGHT0, GL_AMBIENT,
              (0.2, 0.2, 0.2, 1.0))

    # Luz difusa
    glLightfv(GL_LIGHT0, GL_DIFFUSE,
              (0.9, 0.9, 0.9, 1.0))

    # Luz especular
    glLightfv(GL_LIGHT0, GL_SPECULAR,
              (1.0, 1.0, 1.0, 1.0))

    # Posição da luz
    glLightfv(GL_LIGHT0, GL_POSITION,
              (6.0, 8.0, 12.0, 1.0))

    # Material especular
    glMaterialfv(GL_FRONT_AND_BACK,
                 GL_SPECULAR,
                 (1.0, 1.0, 1.0, 1.0))

    glMaterialf(GL_FRONT_AND_BACK,
                GL_SHININESS,
                64)

    # ----------------------------
    # Câmera
    # ----------------------------
    glMatrixMode(GL_PROJECTION)

    gluPerspective(
        45,
        LARGURA / ALTURA,
        0.1,
        100.0
    )

    glMatrixMode(GL_MODELVIEW)


def atualizar(delta):

    global score
    global game_over

    nave.atualizar(delta)

    # Atualiza projéteis
    for projetil in projeteis[:]:

        projetil.atualizar(delta)

        if not projetil.esta_vivo():
            projeteis.remove(projetil)

    # Atualiza inimigos
    for inimigo in inimigos:
        inimigo.atualizar(delta)

    # Colisões
    pontos, colisao = verificar_colisoes(
        nave,
        projeteis,
        inimigos
    )

    score += pontos

    if colisao:
        game_over = True

    # Mantém sempre seis inimigos
    while len(inimigos) < 6:
        inimigos.append(Inimigo())

    if game_over:
        return


def renderizar():

    if game_over:
        tela_game_over()
        return

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    glTranslatef(0, 0, -25)

    # Atualiza a posição da luz a cada frame
    glLightfv(GL_LIGHT0,
              GL_POSITION,
              (6.0, 8.0, 12.0, 1.0))
    
    desenhar_fundo(textura_fundo)

    # Nave
    nave.desenhar(textura_nave)

    # Projéteis
    for projetil in projeteis:
        projetil.desenhar()

    # Inimigos
    for inimigo in inimigos:
        inimigo.desenhar()

    # Pontuação
    desenhar_texto(f"Pontuação: {score}", 15, 15)

    pygame.display.flip()


def main():

    # Inicializa a janela, OpenGL, texturas, iluminação e recursos do jogo
    inicializar()

    # Relógio responsável por controlar o tempo entre os frames
    clock = pygame.time.Clock()

    # Controla se o jogo continua executando
    executando = True

    # Game Loop principal
    while executando:
        # Esse valor é usado para movimentação independente do FPS 
        # Calcula quanto tempo passou em segundos desde a última atualização.
        delta = clock.tick(FPS) / 1000.0

        # Captura todos os eventos da janela
        for evento in pygame.event.get():

            # Verifica se o usuário fechou a janela
            if evento.type == QUIT:

                executando = False

            # Verifica eventos de teclado pressionado
            elif evento.type == KEYDOWN:

                # Caso a partida tenha terminado,
                # aceita apenas comandos da tela de Game Over
                if game_over:

                    # ESC encerra o jogo
                    if evento.key == K_ESCAPE:
                        executando = False

                    # ENTER reinicia a partida
                    elif evento.key == K_RETURN:
                        reiniciar_jogo()

                    # Impede que os comandos normais do jogo
                    # sejam executados durante o Game Over
                    continue

                # ESC durante o jogo encerra a aplicação
                if evento.key == K_ESCAPE:
                    executando = False

                # Espaço dispara um novo projétil
                elif evento.key == K_SPACE:

                    # Cria um projétil na posição atual da nave,
                    # utilizando o mesmo ângulo de orientação dela
                    projeteis.append(

                        Projetil(
                            nave.x,
                            nave.y,
                            nave.angulo
                        )

                    )

        # Atualiza a lógica do jogo:
        atualizar(delta)

        # Desenha todos os elementos da cena:
        renderizar()

    # Libera os recursos do pygame ao sair do loop
    pygame.quit()

if __name__ == "__main__":
    main()