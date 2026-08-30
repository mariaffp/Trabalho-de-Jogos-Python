import pygame
from grid import Grid, Cell


pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

WIDTH   =  800; HEIGHT =  600
screen = pygame.display.set_mode((WIDTH, HEIGHT))


font_size = 30
font = pygame.font.Font(None, font_size)

idle = pygame.image.load("images/duck/base.png").convert_alpha()
step = pygame.image.load("images/duck/step.png").convert_alpha()
quack = pygame.image.load("images/duck/quack.png").convert_alpha()
dead = pygame.image.load("images/duck/blink.png").convert_alpha() #foi um teste mal feito


# número de celulas
grid_size = (10, 15)


# Cria a janela
WIDTH   =  1000; HEIGHT =  1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# cria a grade
grid = Grid(0, 0, [], grid_size)

# criar objetos, adicione eles a lista
objects = []
objects.append(grid)

# posição inicial do pato do jogador
player_row = 2
player_col = 2

# posição do outro pato(inimigo)
enemy_row = 7
enemy_col = 12

# posição inicial do pato inimigo
enemy_start_row = 7
enemy_start_col = 12

# sprite desse outro pato
enemy_sprite = idle

# pontuação
score = 0

game_time = 0

# tempo do poder
power_time = 0

# sprite atual
current_sprite = idle

# tempo do inimigo
enemy_time = 0

# pequeno manual
manual1 = "Colete os pontinhos!"
manual2 = "Fuja do pato inimigo!"
manual3 = "Use o QUACK no momento certo!"



def move_player(row_change, col_change):
    global player_row
    global player_col
    global score

    new_row = player_row + row_change
    new_col = player_col + col_change

    if not grid.is_wall(new_row, new_col):
        player_row = new_row
        player_col = new_col

        cell = grid.get_cell(player_row, player_col)

        if cell is not None:
            if cell.has_dot:
                cell.has_dot = False
                score += 10


while True:

    dt = clock.tick(10)
    game_time += dt
    enemy_time += dt
    if enemy_time >= 500:
        enemy_time = 0

    # lógica do pato inimigo tentando se aproximar do jogador
        if enemy_row < player_row and not grid.is_wall(enemy_row + 1, enemy_col):
            enemy_row += 1

        elif enemy_row > player_row and not grid.is_wall(enemy_row - 1, enemy_col):
            enemy_row -= 1

        elif enemy_col < player_col and not grid.is_wall(enemy_row, enemy_col + 1):
            enemy_col += 1

        elif enemy_col > player_col and not grid.is_wall(enemy_row, enemy_col - 1):
            enemy_col -= 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        # uso do mouse é obrigatório
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]: # 0 botão esquedo 2, direito

                mouse_x, mouse_y = pygame.mouse.get_pos()

                col = mouse_x // grid.cell_size
                row = mouse_y // grid.cell_size

                cell = grid.get_cell(row, col)

                # se clicar em uma célula livre ativa o quack por um breve tempo
                if cell is not None:
                    if cell.cell_type == "empty":
                        power_time = 1500
                #uso do quack meio que te protege do pato inimigo(pois ele desce pontos quando encosta sem quack)

        # uso do teclado para controle é obnrigatório
        elif event.type == pygame.KEYDOWN:
            #inclua outras funcionalidades para outras téclas
            if event.key == pygame.K_ESCAPE:
                exit()

            elif event.key == pygame.K_UP:
                move_player(-1, 0)
                current_sprite = step

            elif event.key == pygame.K_DOWN:
                move_player(1, 0)
                current_sprite = step

            elif event.key == pygame.K_LEFT:
                move_player(0, -1)
                current_sprite = step

            elif event.key == pygame.K_RIGHT:
                move_player(0, 1)
                current_sprite = step

    #verifica se os patos se encontraram
    if player_row == enemy_row and player_col == enemy_col:

    #diminui o tempo do poder
        if power_time > 0:
            enemy_row = enemy_start_row
            enemy_col = enemy_start_col
            score += 20
        else:
            player_row = 2
            player_col = 2
            enemy_row = enemy_start_row
            enemy_col = enemy_start_col
            score -= 100

            if power_time < 0:
                power_time = dt
                current_sprite = idle


    #quando o poder está ativo, usa quack
    if power_time > 0:
        power_time -= dt
        if power_time <= 0:
            power_time = 0
            current_sprite = idle
    if power_time > 0:
        current_sprite = quack

    if score <= -10:
        current_sprite = dead
        print("Fim de jogo")
        break

    #atualiza
    for obj in objects:
        obj.update(1)

    screen.fill((30, 30, 30))

    for obj in objects:
        obj.draw(screen)

    #desenha o pato do jogador
    player_x = player_col * grid.cell_size
    player_y = player_row * grid.cell_size

    #ajusta o tamanho da imagem
    player_sprite = pygame.transform.scale(
        current_sprite,
        (
            grid.cell_size,
            grid.cell_size
        )
    )

    screen.blit(
        player_sprite,
        (player_x, player_y)
    )
    enemy_x = enemy_col * grid.cell_size
    enemy_y = enemy_row * grid.cell_size

    enemy_image = pygame.transform.scale(
        enemy_sprite,
        (
            grid.cell_size,
            grid.cell_size
        )
    )

    screen.blit(
        enemy_image,
        (enemy_x, enemy_y)
    )

    #pontuação
    score_text = font.render(
        f"Pontuação: {score}",
        True,
        (163, 73, 164)
    )

    screen.blit(
        score_text,
        (610, 30)
    )

    time_text = font.render(
        f"Tempo: {game_time // 1000}s",
        True,
        (163, 73, 164)
    )
    
    screen.blit(
        time_text,
        (610, 100)
    )

    manual1text = font.render(
        (manual1),
        True,
        (255, 255, 255)
    )
    manual2text = font.render(
        (manual2),
        True,
        (255, 255, 255)
    )
    manual3text = font.render(
        (manual3),
        True,
        (255, 255, 255)
    )
    screen.blit(manual1text, (610, 130))
    screen.blit(manual2text, (610, 160))
    screen.blit(manual3text, (610, 190))

    #poder
    if power_time > 0:
        power_text = font.render(
            "QUACK!",
            True,
            (255, 255, 0)
        )
    else:
        power_text = font.render(
            "Normal",
            True,
            (163, 73, 164)
        )

    screen.blit(
        power_text,
        (610, 65)
    )

    pygame.display.flip()