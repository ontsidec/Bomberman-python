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
        self.player = Image.open("res/images/player.png")  # 3
        self.bomb = Image.open("res/images/bomb.png")  # 4
        self.explosion = Image.open("res/images/explosion.png")  # 5
        self.background = Image.new('RGB', (self.tile_width * self.width, self.tile_height * self.height))

        # Tworzenie murów
        for i in range(self.width):
            for j in range(self.height):
                self.tiles[i, j] = 0

        # Tworzenie trawy
        for i in range(1, self.width - 1):
            for j in range(1, self.height - 1):
                self.tiles[i, j] = 1

        # Tworzenie losowej siatki zniszczalnych murów
        for i in range(1, self.width - 1):
            for j in range(1, self.height - 1):
                self.tiles[i, j] = random.randint(1, 2)
        self.tiles[2::2, ::2] = 0  # Zapełnienie siatką murów co 2 wiersz i kolumnę

        # Czyszczenie pól startowych graczy i umiejscowienie graczy na polach startowych
        if self.players <= 2:
            for i, j in ([1, 1], [self.width - 2, self.height - 2]):
                for k in [j - 1, j, j + 1]:
                    if self.tiles[i, k] != 0:
                        self.tiles[i, k] = 1
                for k in [i - 1, i, i + 1]:
                    if self.tiles[k, j] != 0:
                        self.tiles[k, j] = 1
                self.tiles[i, j] = 3

        if self.players == 3:
            p = 3
            for i in [1, self.width - 2]:
                for j in [self.height - 2, 1]:
                    if p != 0:
                        for k in [j - 1, j, j + 1]:
                            if self.tiles[i, k] != 0:
                                self.tiles[i, k] = 1
                        for k in [i - 1, i, i + 1]:
                            if self.tiles[k, j] != 0:
                                self.tiles[k, j] = 1
                        self.tiles[i, j] = 3
                        p -= 1

        if self.players >= 4:
            for i in [1, self.width - 2]:
                for j in [1, self.height - 2]:
                    for k in [j - 1, j, j + 1]:
                        if self.tiles[i, k] != 0:
                            self.tiles[i, k] = 1
                    for k in [i - 1, i, i + 1]:
                        if self.tiles[k, j] != 0:
                            self.tiles[k, j] = 1
                    self.tiles[i, j] = 3

    def display(self):
        """Wyświetlenie planszy"""
        for i in range(self.width):
            for j in range(self.height):
                if self.tiles[i, j] == 0:
                    self.background.paste(self.wall, (i * self.tile_width, j * self.tile_height))
                elif self.tiles[i, j] == 1:
                    self.background.paste(self.grass, (i * self.tile_width, j * self.tile_height))
                elif self.tiles[i, j] == 2:
                    self.background.paste(self.brick, (i * self.tile_width, j * self.tile_height))
                elif self.tiles[i, j] == 3:
                    self.background.paste(self.player, (i * self.tile_width, j * self.tile_height))
                elif self.tiles[i, j] == 4:
                    self.background.paste(self.bomb, (i * self.tile_width, j * self.tile_height))
                elif self.tiles[i, j] == 5:
                    self.background.paste(self.explosion, (i * self.tile_width, j * self.tile_height))
                else:
                    self.background.paste(self.wall, (i * self.tile_width, j * self.tile_height))
        self.background.show()

    def place_bomb(self, x, y):
        """Ustawienie bomby na danej pozycji

            Args:
                x (int): Pozycja x bomby
                y (int): Pozycja y bomby

        """
        if x != 0 and y != 0:
            self.tiles[x, y] = 4

    def check_move(self, x, y):
        """Zwraca aktualną pozycje gracza

            Args:
                x (int): Pozycja x ruchu do sprawdzenia
                y (int): Pozycja y ruchu do sprawdzenia

            Returns:
                True - jeżeli jest możliwy taki ruch

        """
        if self.tiles[x, y] != 0 and self.tiles[x, y] != 2:
            return True
        else:
            return False

    def explode(self, x, y):
        """Tworzy efekt eksplozji bomby

            Args:
                x (int): Pozycja x początku eksplozji
                y (int): Pozycja y początku eksplozji

        """
        for i in [x, x - 1, x - 2, x - 3, x - 4, x - 5]:
            if self.tiles[i, y] == 2:
                self.tiles[i, y] = 5
                break
            if self.tiles[i, y] != 0:
                self.tiles[i, y] = 5
            else:
                break

        for i in [x + 1, x + 2, x + 3, x + 4, x + 5]:
            if self.tiles[i, y] == 2:
                self.tiles[i, y] = 5
                break
            if self.tiles[i, y] != 0:
                self.tiles[i, y] = 5
            else:
                break

        for i in [y, y - 1, y - 2, y - 3, y - 4, y - 5]:
            if self.tiles[x, i] == 2:
                self.tiles[x, i] = 5
                break
            if self.tiles[x, i] != 0:
                self.tiles[x, i] = 5
            else:
                break

        for i in [y + 1, y + 2, y + 3, y + 4, y + 5]:
            if self.tiles[x, i] == 2:
                self.tiles[x, i] = 5
                break
            if self.tiles[x, i] != 0:
                self.tiles[x, i] = 5
            else:
                break
