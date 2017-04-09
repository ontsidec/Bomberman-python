import numpy as np
from PIL import Image
import random


class Board(object):
    """Klasa obsługująca tworzenie i zarządzanie planszą."""
    def __init__(self, width, height, players):
        """Domyślne ustawienia klasy

            Args:
                width (int): Szerokość planszy
                height (int): Wysokość planszy
                players (int): Ilość wszystkich graczy

        """
        self.width = width
        self.height = height
        self.players = players

        self.tile_width = 32
        self.tile_height = 32
        self.tiles = np.zeros((self.width, self.height))

        self.wall = Image.open("res/images/wall.png")  # 0
        self.grass = Image.open("res/images/grass.png")  # 1
        self.brick = Image.open("res/images/brick.png")  # 2
        self.background = Image.new('RGB', (self.tile_width * self.width, self.tile_height * self.height))

        # Tworzenie siatki murów
        for i in range(1, self.width - 1):
            for j in range(1, self.height - 1):
                self.tiles[i, j] = 1

        # Tworzenie losowej siatki zniszczalnych murów
        for i in range(1, self.width - 1):
            for j in range(1, self.height - 1):
                self.tiles[i, j] = random.randint(1, 2)
        self.tiles[2::2, ::2] = 0  # Zapełnienie siatką murów co 2 wiersz i kolumnę

        # TODO Czyszczenie pól startowych
        # TODO Umiejscowienie graczy na polach startowych
        for i in range(self.width):
            for j in range(self.height):
                if self.tiles[i, j] == 1:
                    self.background.paste(self.grass, (i * self.tile_width, j * self.tile_height))
                elif self.tiles[i, j] == 2:
                    self.background.paste(self.brick, (i * self.tile_width, j * self.tile_height))
                else:
                    self.background.paste(self.wall, (i * self.tile_width, j * self.tile_height))

        self.background.show()

Board(21, 21, 2)
