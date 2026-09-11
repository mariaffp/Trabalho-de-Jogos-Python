import pygame
import random
from player import Player
from bullet import sinBullet
from enemy import Enemy, GameWorld
from util import EventHandler, circle_collistiion
import math

#inicialização

pygame.init()
WIDTH   =  800; HEIGHT =  600
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))  
player = Player((50, 50))
GameWorld.player = player
#b = sinBullet((400, 300), -45, life_time=240) 

objects = []
objects.append(player)
enemies = []

bullets = []

# controle dos inimigos
spawn_timer = 0
spawn_interval = 2

# para o poder das balas orbitais
orbital_bullets = []

# funções auxiliares

def handle_input(player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.action_1() # pode ser melhorado para evento
            if event.key == pygame.K_TAB:
                player.action_2() # pode ser melhorado para evento
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.shoot(pygame.mouse.get_pos())

def remove_obj(obj):
    #variavel global é feio, mas serve como um exemplo
    if obj in objects:
        objects.remove(obj)

def remove_enemy(enemy):
    if enemy in enemies:
        enemies.remove(enemy)

def create_bullet(data):
    bullet = sinBullet(
        data["pos"],
        velocity=data["velocity"],
        life_time=120
    )

    bullets.append(bullet)

def power_up(player):
    orbital_bullets.clear()

    for i in range(12):
        angle = i * 30

        orbital_bullets.append({
            "angle": angle,
            "pos": player.pos.copy()
        })

def remove_bullet(bullet):
    if bullet in bullets:
        bullets.remove(bullet)


#inscreve esse metodo pra remoção de objetos
EventHandler().subscribe("DestroyObj", remove_bullet)

EventHandler().subscribe("CreateBullet", create_bullet)
#evento de remover o inimigo quando acertado
EventHandler().subscribe("EnemyKilled", remove_enemy)

#evento do poderzinho
EventHandler().subscribe("PowerUp", power_up)

# loop principal

running = True
while running:

    handle_input(player)

    for obj in objects:
        obj.update(1)

    # cria inimigos de tempos em tempos
    spawn_timer += 1

    if spawn_timer >= spawn_interval * 60:
        spawn_timer = 0

        side = random.randint(0, 3)

        if side == 0:
            pos = (random.randint(0, WIDTH), -30)
        elif side == 1:
            pos = (WIDTH + 30, random.randint(0, HEIGHT))
        elif side == 2:
            pos = (random.randint(0, WIDTH), HEIGHT + 30)
        else:
            pos = (-30, random.randint(0, HEIGHT))

        enemies.append(Enemy(pos))

    # atualiza os inimigos
    for enemy in enemies:
        enemy.update(1)

    for bullet in bullets:
        bullet.update(1)

    for orbital in orbital_bullets:
        orbital["angle"] += 3

        angle = math.radians(orbital["angle"])

        orbital["pos"] = pygame.Vector2(
            player.pos.x + math.cos(angle) * 70,
            player.pos.y + math.sin(angle) * 70
        )
        if player.state.__class__.__name__ != "AttackState":
            orbital_bullets.clear()

    # ver a colisão
    for bullet in bullets:
        for enemy in enemies:
            if circle_collistiion(
                bullet.pos,
                bullet.radius,
                enemy.pos,
                enemy.radius
            ):
                enemy.hit()
                bullet.destroy()
                break

    # adicionar a colisão pras balas orbitais tambem!
    for orbital in orbital_bullets:
        for enemy in enemies:
            if circle_collistiion(
                orbital["pos"],
                6,
                enemy.pos,
                enemy.radius
            ):
                enemy.hit()
                break
            
    for enemy in enemies:
        if circle_collistiion(
            enemy.pos,
            enemy.radius,
            player.pos,
            player.radius
        ):
            player.take_damage()

    screen.fill((190, 175, 210))

    for obj in objects:
        obj.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)

    for orbital in orbital_bullets:
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(orbital["pos"].x), int(orbital["pos"].y)),
            6
        )
        
    pygame.display.flip()
    clock.tick(60)
    