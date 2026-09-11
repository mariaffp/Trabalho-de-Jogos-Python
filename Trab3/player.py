import pygame
from abc import ABC, abstractmethod
from util import colored_sprite, EventHandler


class Player:

    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.speed = 4
        self.radius = 16

        # vida do jogador
        self.health = 5

        # começa no estado normal
        self.state = NormalState(self)

    def update(self, dt):
        self.state.update(dt)

    def draw(self, screen):
        self.state.draw(screen)

    def action_1(self):
        self.state.action_1()

    def action_2(self):
        self.state.action_2()

    def shoot(self, target):
        self.state.shoot(target)

    def take_damage(self):
        self.state.take_damage()

    def change_state(self, new_state):
        self.state.delete()
        self.state = new_state(self)


class PlayerState(ABC):

    # Sprite é comum a classe estado
    sprite = pygame.Surface((32, 32))

    def __init__(self, player):
        self.P = player
        self.sprite = pygame.image.load("images/duck/base.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (60, 60))

    def draw(self, screen):
        screen.blit(
            self.sprite,
            (
                int(self.P.pos.x - 16),
                int(self.P.pos.y - 16)
            )
        )

    def delete(self):
        pass  # se precisar apagar algo na mudança de estados

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def action_1(self):
        pass

    def shoot(self, target):
        pass

    def take_damage(self):
        pass

    @abstractmethod
    def action_2(self):
        pass


class NormalState(PlayerState):

    # Estado normal do jogador
    #sprite = colored_sprite((80, 220, 255))
    sprite = None

    def update(self, dt):

        keys = pygame.key.get_pressed()

        movement = pygame.Vector2(0, 0)

        if keys[pygame.K_w]:
            movement.y -= 1
        if keys[pygame.K_s]:
            movement.y += 1
        if keys[pygame.K_a]:
            movement.x -= 1
        if keys[pygame.K_d]:
            movement.x += 1

        if movement.length() > 0:
            movement = movement.normalize()
            self.P.pos += movement * self.P.speed * dt

        # não deixa o jogador sair da tela
        self.P.pos.x = max(16, min(784, self.P.pos.x))
        self.P.pos.y = max(16, min(584, self.P.pos.y))

    def action_1(self):
        # disparo será implementado depois
        EventHandler().notify("Shoot", self.P)

    def shoot(self, target):
        direction = pygame.Vector2(target) - self.P.pos

        if direction.length() == 0:
            return

        direction = direction.normalize()

        EventHandler().notify(
            "CreateBullet",
            {
                "pos": self.P.pos.copy(),
                "velocity": direction * 8
            }
        )

    def take_damage(self):
        # recebe dano
        self.P.health -= 1

        EventHandler().notify("PlayerDamaged", self.P)

        if self.P.health <= 0:
            EventHandler().notify("GameOver", self.P)
        else:
            self.P.change_state(InvincibleState)

    def action_2(self):
        EventHandler().notify("PowerUp", self.P)
        self.P.change_state(AttackState)


class InvincibleState(PlayerState):

    # Estado temporário depois que o jogador recebe dano
    sprite = colored_sprite((255, 255, 255))

    def __init__(self, player):
        super().__init__(player)
        self.sprite = pygame.image.load("images/duck/blink.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (60, 60))
        self.elapsed = 0
        self.duration = 180

    def update(self, dt):

        self.elapsed += dt

        # continua permitindo movimentação
        keys = pygame.key.get_pressed()

        movement = pygame.Vector2(0, 0)

        if keys[pygame.K_w]:
            movement.y -= 1
        if keys[pygame.K_s]:
            movement.y += 1
        if keys[pygame.K_a]:
            movement.x -= 1
        if keys[pygame.K_d]:
            movement.x += 1

        if movement.length() > 0:
            movement = movement.normalize()
            self.P.pos += movement * self.P.speed * dt

        self.P.pos.x = max(16, min(784, self.P.pos.x))
        self.P.pos.y = max(16, min(584, self.P.pos.y))

        # depois do tempo volta ao estado normal
        if self.elapsed >= self.duration:
            self.P.change_state(NormalState)

    def draw(self, screen):
        # pisca enquanto está invencível
        if int(self.elapsed * 5) % 2 == 0:
            super().draw(screen)

    def action_1(self):
        EventHandler().notify("Shoot", self.P)

    def shoot(self, target):
        NormalState(self.P).shoot(target)

    def take_damage(self):
        # enquanto está invencível, não recebe dano novamente
        pass

    def action_2(self):
        # enquanto está invencível, não recebe dano novamente
        pass

class AttackState(PlayerState):

    def __init__(self, player):
        super().__init__(player)

        self.sprite = pygame.image.load(
            "images/duck/quack.png"
        ).convert_alpha()

        self.sprite = pygame.transform.scale(
            self.sprite,
            (60, 60)
        )

        self.elapsed = 0
        self.duration = 180

    def update(self, dt):
        self.elapsed += dt

        # continua permitindo movimentação durante o poder
        keys = pygame.key.get_pressed()
        movement = pygame.Vector2(0, 0)

        if keys[pygame.K_w]:
            movement.y -= 1
        if keys[pygame.K_s]:
            movement.y += 1
        if keys[pygame.K_a]:
            movement.x -= 1
        if keys[pygame.K_d]:
            movement.x += 1

        if movement.length() > 0:
            movement = movement.normalize()
            self.P.pos += movement * self.P.speed * dt

        self.P.pos.x = max(16, min(784, self.P.pos.x))
        self.P.pos.y = max(16, min(584, self.P.pos.y))

        # depois de 3 segundos volta ao estado normal
        if self.elapsed >= self.duration:
            self.P.change_state(NormalState)

    def action_1(self):
        pass

    def shoot(self, target):
        # continua permitindo tiro normal durante o poder
        NormalState(self.P).shoot(target)

    def action_2(self):
        pass

    def take_damage(self):
        self.P.health -= 1