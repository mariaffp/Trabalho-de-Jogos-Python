import pygame
from abc import ABC, abstractmethod
from util import colored_sprite, EventHandler, circle_collistiion


class Enemy:

    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.speed = 1.2
        self.radius = 16
        self.health = 2

        # começa se aproximando do jogador
        self.state = ApproachingState(self)

    def update(self, dt):
        self.state.update(dt)

    def draw(self, screen):
        self.state.draw(screen)

    def hit(self):
        self.state.hit()

    def change_state(self, new_state):
        self.state.delete()
        self.state = new_state(self)


class EnemyState(ABC):

    # Sprite é comum a classe estado
    sprite = pygame.Surface((32, 32))

    def __init__(self, enemy):
        self.E = enemy
        self.sprite = pygame.image.load(
            "images/duck/crouch.png"
        ).convert_alpha()
        self.sprite = pygame.transform.scale(
            self.sprite,
            (48, 48)
        )

    def draw(self, screen):
        screen.blit(
            self.sprite,
            (
                int(self.E.pos.x - 16),
                int(self.E.pos.y - 16)
            )
        )

    def delete(self):
        pass  # se precisar apagar algo na mudança de estados

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def hit(self):
        pass


class ApproachingState(EnemyState):

    # Estado em que o inimigo se aproxima do jogador
    sprite = colored_sprite((220, 60, 80))

    def update(self, dt):

        # jogador será definido pelo jogo
        player = GameWorld.player

        direction = player.pos - self.E.pos

        if direction.length() > 0:
            direction = direction.normalize()
            self.E.pos += direction * self.E.speed * dt

    def hit(self):

        self.E.health -= 1

        if self.E.health <= 0:
            EventHandler().notify("EnemyKilled", self.E)
        else:
            # depois de ser atingido, fica atordoado
            self.E.change_state(StunnedState)


class StunnedState(EnemyState):

    # Estado temporário depois que o inimigo é atingido
    #sprite = colored_sprite((180, 100, 230))

    def __init__(self, enemy):
        super().__init__(enemy)
        self.sprite = pygame.image.load(
            "images/duck/wing.png"
        ).convert_alpha()

        self.sprite = pygame.transform.scale(
            self.sprite,
            (48, 48)
        )
        self.elapsed = 0
        self.duration = 45

    def update(self, dt):

        self.elapsed += dt

        # depois do atordoamento volta a perseguir
        if self.elapsed >= self.duration:
            self.E.change_state(ApproachingState)

    def hit(self):

        # ainda pode receber dano enquanto está atordoado
        self.E.health -= 1

        if self.E.health <= 0:
            EventHandler().notify("EnemyKilled", self.E)


class GameWorld:
    # referência ao jogador para os inimigos conseguirem encontrá-lo
    player = None