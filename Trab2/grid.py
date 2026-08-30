# Classe base abstrata (Abstract Base Class)
from abc import ABC, abstractmethod
import pygame


# objeto herda de classe abstrata
## nunca pode ser criada, só as filhas
class obj (ABC):

    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        #lista
        self.sprites = sprites

    def draw(self, screen):
        for s in self.sprites:
            screen.blit(s, (self.x, self.y))

    # avisa que o método é abstato e precisa ser feito pelos filhos
    @abstractmethod
    def update(self, dt):
        pass


class Grid (obj):

    # só avisa a construtora da mãe o que fazer
    # pode, e deve ser extendido para outras caracteristicas nescessárias
    def __init__(self, x, y, sprites, grid_size):
        # bom lugar para criar uma matriz de celulas
        super().__init__(x, y, sprites)

        self.rows = grid_size[0]
        self.cols = grid_size[1]
        self.cell_size = 40

        self.cells = []

        # mapa da grade
        # 1 é parede
        # 0 é espaço/bloco/célula livre
        map_data = [
            "111111111111111",
            "100000111000001",
            "100000000000001",
            "100001111000001",
            "100000000000001",
            "100000111100001",
            "100000000000001",
            "100000000011001",
            "100000000000001",
            "111111111111111"
        ]

        # cria a matriz de células
        for row in range(self.rows):
            linha = []

            for col in range(self.cols):

                if map_data[row][col] == "1":
                    cell_type = "wall"
                else:
                    cell_type = "empty"

                cell = Cell(
                    col * self.cell_size,
                    row * self.cell_size,
                    [],
                    self.cell_size,
                    cell_type
                )

                # coloca comida nas áreas sem a parede
                if cell_type == "empty":
                    cell.has_dot = True

                linha.append(cell)

            self.cells.append(linha)

    def get_cell(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.cells[row][col]

        return None

    def is_wall(self, row, col):
        cell = self.get_cell(row, col)

        if cell is None:
            return True

        return cell.cell_type == "wall"

    def draw(self, screen):

        # chama o desenha já pronto de obj, mas pode ser extendido
        for row in self.cells:
            for cell in row:
                cell.draw(screen)

    def update(self, dt):
        # não chama o de super, porque ele não implementa, crie seu próprio
        return


class Cell (obj):

    # só avisa a construtora da mãe o que fazer
    # pode, e deve ser extendido para outras caracteristicas nescessárias
    def __init__(self, x, y, sprites, grid_size, cell_type):
        # bom lugar para definir coisas como o fundo da céula
        super().__init__(x, y, sprites)

        self.size = grid_size
        self.cell_type = cell_type
        self.has_dot = False

    def draw(self, screen):

        rect = pygame.Rect(
            self.x,
            self.y,
            self.size,
            self.size
        )

        if self.cell_type == "wall":
            pygame.draw.rect(
                screen,
                (52, 21, 57),
                rect
            )

        else:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                rect
            )

            if self.has_dot:
                pygame.draw.circle(
                    screen,
                    (255, 255, 255),
                    rect.center,
                    3
                )

    def update(self, dt):
        # não chama o de super, porque ele não implementa, crie seu próprio
        return