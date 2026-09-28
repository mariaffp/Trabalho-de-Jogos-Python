import math
import pygame
from shape import Polygon
from collision import Collide
from events import event_bus

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


# -------------------------------------------------------------
# Example
# -------------------------------------------------------------

polygon_a = Polygon([
    (190, 80),
    (205, 75),
    (220, 80),
    (225, 95),
    (220, 110),
    (205, 115),
    (190, 110),
    (185, 95),
])

polygon_c = Polygon([
    (580, 150),
    (650, 130),
    (700, 180),
    (670, 230),
    (600, 220),
])

polygon_vel = Polygon([
    (80, 170),
    (140, 140),
    (190, 170),
    (170, 230),
    (110, 240),
])

# blocos que fecham a mesa embaixo e formam o funil até as abas
bloco_esquerdo = Polygon([
    (0, 410),
    (240, 497),
    (240, 600),
    (0, 600),
])

bloco_direito = Polygon([
    (800, 410),
    (560, 497),
    (560, 600),
    (800, 600),
])


class Inimigo:
    # estados: aproximando, atordoado, destruido
    HP_MAX = 3
    ATORDOADO_DURACAO = 20
    RENASCER_DURACAO = 360
    COR_BASE = (150, 30, 60)
    COR_ATORDOADO = (235, 200, 210)

    def __init__(self, points, fase=0):
        self.polygon = Polygon(points)
        self.hp = self.HP_MAX
        self.estado = "aproximando"
        self.timer = 0
        self.pulso = fase

    def renascer(self):
        self.hp = self.HP_MAX
        self.estado = "aproximando"
        self.timer = 0

    def atualizar(self):
        self.pulso += 1

        if self.estado == "atordoado":
            self.timer -= 1

            if self.timer <= 0:
                self.estado = "aproximando"

            self.polygon.color = self.COR_ATORDOADO

        elif self.estado == "destruido":
            self.timer -= 1

            if self.timer <= 0:
                self.renascer()

        else:
            # "respirando" pra dar a sensação de ameaça se aproximando
            brilho = int(20 * math.sin(self.pulso * 0.05))
            r, g, b = self.COR_BASE
            self.polygon.color = (r + brilho, g + brilho, b + brilho)


class Aba:
    # estados: repouso, subindo, ativa, descendo
    COMPRIMENTO = 125
    ANGULO_REPOUSO = 28
    ANGULO_ATIVO = -28
    VELOCIDADE = 7
    VELOCIDADE_REFORCADA = 11
    COR_NORMAL = (120, 70, 160)
    COR_REFORCADA = (180, 130, 220)

    def __init__(self, pivo, lado):
        # lado: 1 aba esquerda (aponta pra direita), -1 aba direita
        self.pivo = pivo
        self.lado = lado
        self.angulo = self.ANGULO_REPOUSO
        self.velocidade_angular = 0
        self.estado = "repouso"
        self.polygon = Polygon(self.pontos())
        self.polygon.color = self.COR_NORMAL

    def pontos(self):
        a = math.radians(self.angulo)
        dx = self.lado * math.cos(a)
        dy = math.sin(a)
        nx, ny = -dy, dx
        px, py = self.pivo
        tx = px + dx * self.COMPRIMENTO
        ty = py + dy * self.COMPRIMENTO

        return [
            (px + nx * 11, py + ny * 11),
            (tx + nx * 6, ty + ny * 6),
            (tx - nx * 6, ty - ny * 6),
            (px - nx * 11, py - ny * 11),
        ]

    def atualizar(self, pressionada, reforcada):
        alvo = self.ANGULO_ATIVO if pressionada else self.ANGULO_REPOUSO
        velocidade = self.VELOCIDADE_REFORCADA if reforcada else self.VELOCIDADE
        diferenca = alvo - self.angulo

        if abs(diferenca) <= velocidade:
            self.angulo = alvo
            self.velocidade_angular = 0
        else:
            passo = velocidade if diferenca > 0 else -velocidade
            self.angulo += passo
            self.velocidade_angular = passo

        if self.velocidade_angular < 0:
            self.estado = "subindo"
        elif self.velocidade_angular > 0:
            self.estado = "descendo"
        elif self.angulo == self.ANGULO_ATIVO:
            self.estado = "ativa"
        else:
            self.estado = "repouso"

        self.polygon.color = self.COR_REFORCADA if reforcada else self.COR_NORMAL
        self.polygon.points = self.pontos()
        self.polygon.update_geometry()

    def velocidade_em(self, ponto):
        # velocidade da superfície da aba no ponto onde a bola encosta
        rx = ponto[0] - self.pivo[0]
        ry = ponto[1] - self.pivo[1]
        w = math.radians(self.velocidade_angular)

        return (-ry * w * self.lado, rx * w * self.lado)


# inimigos lá em cima, funcionam como obstáculos que aguentam alguns hits
inimigos = [
    Inimigo([
        (360, 150),
        (380, 115),
        (420, 115),
        (440, 150),
        (420, 185),
        (380, 185),
    ], 0),
    Inimigo([
        (250, 290),
        (290, 255),
        (330, 290),
        (315, 325),
        (265, 325),
    ], 40),
    Inimigo([
        (470, 290),
        (510, 255),
        (550, 290),
        (535, 325),
        (485, 325),
    ], 80),
]

abas = [
    Aba((235, 505), 1),
    Aba((565, 505), -1),
]

polygons = [
    polygon_a,
    bloco_esquerdo,
    bloco_direito,
    polygon_c,
    polygon_vel,
]

# estado da bola
ball_velocity_x = 2
ball_velocity_y = 0
gravity = 0.2
VELOCIDADE_MAXIMA = 15

score = 0
lives = 3

bonus_used = False
vel_usada = False

esquerda = False
direita = False

fim_jogo = False

shape_a = None
shape_b = None

# enquanto o reforço estiver ativo, as abas giram mais rápido
torre_reforco_timer = 0
TORRE_REFORCO_DURACAO = 300  # ~5s a 60fps

# cores (paleta roxo escuro / vinho)
COR_FUNDO = (22, 12, 30)
COR_TEXTO = (230, 220, 235)

polygon_a.color = (235, 195, 90)       # bola
polygon_c.color = (180, 60, 120)       # bônus de pontos
polygon_vel.color = (210, 120, 60)     # bônus de velocidade
bloco_esquerdo.color = (52, 30, 68)    # blocos do funil
bloco_direito.color = (52, 30, 68)


def reset_ball():
    global ball_velocity_x
    global ball_velocity_y
    global bonus_used
    global vel_usada

    polygon_a.points = [
        (190, 80),
        (205, 75),
        (220, 80),
        (225, 95),
        (220, 110),
        (205, 115),
        (190, 110),
        (185, 95),
    ]

    polygon_a.update_geometry()

    ball_velocity_x = 2
    ball_velocity_y = 0

    bonus_used = False
    vel_usada = False


def resolver_colisao_solida(alvo, elasticidade=0.6, velocidade_alvo=(0, 0)):
    # empurra a bola pra fora da sobreposição e reflete a velocidade
    # em torno do eixo de colisão, em vez de só inverter x ou y
    global ball_velocity_x, ball_velocity_y

    resultado = Collide.polygon_mtv(polygon_a, alvo)

    if not resultado:
        return None

    shape_a, shape_b, eixo, sobreposicao = resultado

    centro_bola = polygon_a.bounding_box.center
    centro_alvo = alvo.bounding_box.center

    dx = centro_bola[0] - centro_alvo[0]
    dy = centro_bola[1] - centro_alvo[1]

    # garante que o eixo aponta pra fora do alvo, não pra dentro
    if dx * eixo[0] + dy * eixo[1] < 0:
        eixo = (-eixo[0], -eixo[1])

    polygon_a.points = [
        (x + eixo[0] * sobreposicao, y + eixo[1] * sobreposicao)
        for x, y in polygon_a.points
    ]
    polygon_a.update_geometry()

    # velocidade da bola em relação ao alvo (que pode estar se mexendo)
    rel_x = ball_velocity_x - velocidade_alvo[0]
    rel_y = ball_velocity_y - velocidade_alvo[1]
    produto = rel_x * eixo[0] + rel_y * eixo[1]

    # só reflete se a bola estiver indo de encontro ao alvo
    if produto < 0:

        # encostos leves (rolando) não quicam, senão a bola vibra
        if -produto < 1.0:
            elasticidade = 0

        ball_velocity_x -= (1 + elasticidade) * produto * eixo[0]
        ball_velocity_y -= (1 + elasticidade) * produto * eixo[1]

    return shape_a, shape_b


def lose_life():
    global lives
    global fim_jogo
    global score

    lives -= 1
    score -= 10

    if lives <= 0:
        fim_jogo = True
    else:
        reset_ball()


# --- reações aos eventos ---
# quem dispara o evento não precisa saber o que acontece com o placar/vida,
# só avisa que aconteceu

def _ao_atingir_inimigo(inimigo, dano):
    global score
    score += 5


def _ao_destruir_inimigo(inimigo, pontos):
    global score
    score += pontos
    inimigo.estado = "destruido"
    inimigo.timer = Inimigo.RENASCER_DURACAO


def _ao_coletar_powerup(tipo):
    global score, torre_reforco_timer

    if tipo == "pontos":
        score += 50
    elif tipo == "velocidade":
        score += 20
        torre_reforco_timer = TORRE_REFORCO_DURACAO


def _ao_perder_vida():
    lose_life()


event_bus.on("inimigo_atingido", _ao_atingir_inimigo)
event_bus.on("inimigo_destruido", _ao_destruir_inimigo)
event_bus.on("powerup_coletado", _ao_coletar_powerup)
event_bus.on("vida_perdida", _ao_perder_vida)


running = True

while running:

    if not fim_jogo:

        ball_velocity_y += gravity

        velocidade = math.hypot(ball_velocity_x, ball_velocity_y)

        if velocidade > VELOCIDADE_MAXIMA:
            ball_velocity_x *= VELOCIDADE_MAXIMA / velocidade
            ball_velocity_y *= VELOCIDADE_MAXIMA / velocidade

        for i in range(len(polygon_a.points)):
            x, y = polygon_a.points[i]

            polygon_a.points[i] = (
                x + ball_velocity_x,
                y + ball_velocity_y
            )

        polygon_a.update_geometry()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and Polygon.debug:

                # Try to select a vertex from each polygon
                for polygon in polygons + [i.polygon for i in inimigos]:
                    polygon.start_drag(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:

                for polygon in polygons + [i.polygon for i in inimigos]:
                    polygon.stop_drag()

        elif event.type == pygame.MOUSEMOTION:

            for polygon in polygons + [i.polygon for i in inimigos]:
                polygon.drag(event.pos)

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                esquerda = True

            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                direita = True

            elif event.key == pygame.K_F1:
                Polygon.debug = not Polygon.debug

            elif event.key == pygame.K_r and fim_jogo:
                lives = 3
                score = 0
                fim_jogo = False
                reset_ball()
                torre_reforco_timer = 0

                for inimigo in inimigos:
                    inimigo.renascer()

        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                esquerda = False

            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                direita = False

    if not fim_jogo:

        reforcada = torre_reforco_timer > 0

        if reforcada:
            torre_reforco_timer -= 1

        abas[0].atualizar(esquerda, reforcada)
        abas[1].atualizar(direita, reforcada)

        # rebote nas laterais e no topo
        if polygon_a.bounding_box.left <= 0:
            ball_velocity_x = abs(ball_velocity_x)

        if polygon_a.bounding_box.right >= 800:
            ball_velocity_x = -abs(ball_velocity_x)

        if polygon_a.bounding_box.top <= 0:
            ball_velocity_y = abs(ball_velocity_y)

        # blocos do funil
        resolver_colisao_solida(bloco_esquerdo)
        resolver_colisao_solida(bloco_direito)

        # colisão com as abas, a superfície em movimento empurra a bola
        for aba in abas:
            velocidade_aba = aba.velocidade_em(polygon_a.bounding_box.center)

            resolver_colisao_solida(
                aba.polygon,
                elasticidade=0.4,
                velocidade_alvo=velocidade_aba
            )

        # colisão com os inimigos (funcionam como bumpers)
        shape_a = None
        shape_b = None

        for inimigo in inimigos:
            inimigo.atualizar()

            if inimigo.estado == "destruido":
                continue

            collision = resolver_colisao_solida(
                inimigo.polygon,
                elasticidade=1.15
            )

            if collision:

                shape_a, shape_b = collision

                # só conta hit se o inimigo não estiver atordoado ainda
                if inimigo.estado == "aproximando":
                    inimigo.hp -= 1
                    inimigo.estado = "atordoado"
                    inimigo.timer = Inimigo.ATORDOADO_DURACAO

                    if inimigo.hp <= 0:
                        event_bus.emit(
                            "inimigo_destruido",
                            inimigo=inimigo,
                            pontos=50
                        )
                    else:
                        event_bus.emit(
                            "inimigo_atingido",
                            inimigo=inimigo,
                            dano=1
                        )

        # bônus de pontos
        bonus_collision = Collide.polygon(
            polygon_a,
            polygon_c
        )

        if bonus_collision and not bonus_used:
            event_bus.emit("powerup_coletado", tipo="pontos")
            bonus_used = True

        # bônus de velocidade
        vel_collision = Collide.polygon(
            polygon_a,
            polygon_vel
        )

        if vel_collision and not vel_usada:
            ball_velocity_x *= 1.5
            ball_velocity_y *= 1.5
            event_bus.emit("powerup_coletado", tipo="velocidade")
            vel_usada = True

        # espaço entre as abas: a bola cai de verdade e some da tela
        if polygon_a.bounding_box.top > 620:
            event_bus.emit("vida_perdida")

    screen.fill(COR_FUNDO)

    # Draw polygons
    for polygon in polygons:
        polygon.draw(screen)

    for inimigo in inimigos:
        if inimigo.estado != "destruido":
            inimigo.polygon.draw(screen)

    for aba in abas:
        aba.polygon.draw(screen)

    # Collision
    polygon_a.draw(screen, shape_a)

    font = pygame.font.SysFont(None, 30)

    if fim_jogo:

        text = font.render(
            f"Pontos: {score} | Vidas: {lives} | R para reiniciar",
            True,
            COR_TEXTO
        )

    else:

        text = font.render(
            f"Pontos: {score} | Vidas: {lives}",
            True,
            COR_TEXTO
        )

    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()