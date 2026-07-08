import math


def colisao_circulo(x1, y1, r1, x2, y2, r2):
    """
    Verifica colisão entre dois círculos.
    """

    dx = x2 - x1
    dy = y2 - y1

    distancia = math.sqrt(dx * dx + dy * dy)

    return distancia <= (r1 + r2)


def verificar_colisoes(nave, projeteis, inimigos):
    """
    Verifica todas as colisões do jogo.

    Retorna:
        score_ganho
        game_over
    """

    score = 0
    game_over = False

    # -------------------------------
    # Projétil x Inimigo
    # -------------------------------

    for projetil in projeteis[:]:

        for inimigo in inimigos[:]:

            if colisao_circulo(
                projetil.x,
                projetil.y,
                projetil.raio,

                inimigo.x,
                inimigo.y,
                inimigo.raio
            ):

                if projetil in projeteis:
                    projeteis.remove(projetil)

                if inimigo in inimigos:
                    inimigos.remove(inimigo)

                score += 10

                break

    # -------------------------------
    # Nave x Inimigo
    # -------------------------------

    for inimigo in inimigos:

        if colisao_circulo(
            nave.x,
            nave.y,
            nave.raio,

            inimigo.x,
            inimigo.y,
            inimigo.raio
        ):

            game_over = True
            break

    return score, game_over