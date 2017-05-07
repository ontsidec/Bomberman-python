import numpy as np
import random

from src import constants as const
from src import player


class Board(object):
    """Klasa obsługująca tworzenie i zarządzanie planszą."""
    def __init__(self, players):
        """Domyślne ustawienia klasy

            Args:
                players (int): Ilość wszystkich graczy

        """
        self.width = const.BOARD_WIDTH
        self.height = const.BOARD_HEIGHT
        self.tiles = np.zeros((self.width, self.height), dtype=int)

        self.players = players
        self.player_1 = player.Player('Gracz 1', 1, 1)

        self.create_board()
        self.board_history = []

        for x in range(self.width):
            for y in range(self.height):
                    move = '@' + str(x) + '*' + str(y) + '*' + str(self.tiles[x, y]) + '*!'
                    self.board_history.append(move)
        self.board_history.append('#')

    def create_board(self):
        """Tworzenie planszy"""

        # Tworzenie murów
        for i in range(self.width):
            for j in range(self.height):
                self.tiles[i, j] = const.WALL

        # Tworzenie trawy
        for i in range(1, self.width - 1):
            for j in range(1, self.height - 1):
                self.tiles[i, j] = const.GRASS

        # Tworzenie losowej siatki zniszczalnych murów
        for i in range(1, self.width - 1):
            for j in range(1, self.height - 1):
                self.tiles[i, j] = random.randint(const.GRASS, const.WOOD)
        self.tiles[2::2, ::2] = const.WALL  # Zapełnienie siatką murów co 2 wiersz i kolumnę

        # Czyszczenie pól startowych graczy i umiejscowienie graczy na polach startowych
        if self.players == 1:
            for k in [0, 1, 2]:
                if self.tiles[1, k] != const.WALL:
                    self.tiles[1, k] = const.GRASS
            for k in [0, 1, 2]:
                if self.tiles[k, 1] != const.WALL:
                    self.tiles[k, 1] = const.GRASS
            self.tiles[self.player_1.get_pos_x(), self.player_1.get_pos_y()] = const.PLAYER_FRONT

        if self.players == 2:
            for i, j in ([1, 1], [self.width - 2, self.height - 2]):
                for k in [j - 1, j, j + 1]:
                    if self.tiles[i, k] != const.WALL:
                        self.tiles[i, k] = const.GRASS
                for k in [i - 1, i, i + 1]:
                    if self.tiles[k, j] != const.WALL:
                        self.tiles[k, j] = const.GRASS
                self.tiles[i, j] = const.PLAYER_FRONT

        if self.players == 3:
            p = 3
            for i in [1, self.width - 2]:
                for j in [self.height - 2, 1]:
                    if p != 0:
                        for k in [j - 1, j, j + 1]:
                            if self.tiles[i, k] != const.WALL:
                                self.tiles[i, k] = const.GRASS
                        for k in [i - 1, i, i + 1]:
                            if self.tiles[k, j] != const.WALL:
                                self.tiles[k, j] = const.GRASS
                        self.tiles[i, j] = const.PLAYER_FRONT
                        p -= 1

        if self.players >= 4:
            for i in [1, self.width - 2]:
                for j in [1, self.height - 2]:
                    for k in [j - 1, j, j + 1]:
                        if self.tiles[i, k] != const.WALL:
                            self.tiles[i, k] = const.GRASS
                    for k in [i - 1, i, i + 1]:
                        if self.tiles[k, j] != const.WALL:
                            self.tiles[k, j] = const.GRASS
                    self.tiles[i, j] = const.PLAYER_FRONT

    def save_change(self, previous_board):
        """Zapisuje zmianę pól planszy pomiędzy kolejnymi klatkami

            Args:
                previous_board (int array): Poprzednia wersja planszy
        """
        for x in range(self.width):
            for y in range(self.height):
                if previous_board[x, y] != self.tiles[x, y]:
                    move = '@' + str(x) + '*' + str(y) + '*' + str(self.tiles[x, y]) + '*!'
                    self.board_history.append(move)

        self.board_history.append('#')

    def try_move(self, x, y):
        """Zwraca aktualną pozycje gracza

            Args:
                x (int): Pozycja x ruchu do sprawdzenia
                y (int): Pozycja y ruchu do sprawdzenia

            Returns:
                True - jeżeli jest możliwy taki ruch

        """
        if self.tiles[x, y] != const.WALL and self.tiles[x, y] != const.WOOD and self.tiles[x, y] != const.BOMB:
            return True
        else:
            return False

    def move(self, x, y):
        """Przesunięcie gracza na daną pozycje

            Args:
                x (int): Pozycja x bomby
                y (int): Pozycja y bomby

        """
        if self.tiles[self.player_1.get_pos_x(), self.player_1.get_pos_y()] == const.PLAYER_FRONT:
            self.tiles[self.player_1.get_pos_x(), self.player_1.get_pos_y()] = const.GRASS
        else:
            self.tiles[self.player_1.get_pos_x(), self.player_1.get_pos_y()] = const.BOMB
        self.player_1.move(x, y)
        self.tiles[x, y] = const.PLAYER_FRONT

    def place_bomb(self, x, y):
        """Ustawienie bomby na danej pozycji

            Args:
                x (int): Pozycja x bomby
                y (int): Pozycja y bomby

        """
        if x != 0 and y != 0:
            self.tiles[x, y] = const.BOMB

    def explode(self, x, y):
        """Tworzy efekt eksplozji bomby

            Args:
                x (int): Pozycja x początku eksplozji
                y (int): Pozycja y początku eksplozji

        """
        for i in [x, x - 1, x - 2, x - 3, x - 4, x - 5]:
            if self.player_1.get_pos_x() == i and self.player_1.get_pos_y() == y:
                self.player_1.isDead = True
            if self.tiles[i, y] == const.WOOD:
                self.tiles[i, y] = const.EXPLOSION
                break
            if self.tiles[i, y] != const.WALL:
                self.tiles[i, y] = const.EXPLOSION
            else:
                break

        for i in [x + 1, x + 2, x + 3, x + 4, x + 5]:
            if self.player_1.get_pos_x() == i and self.player_1.get_pos_y() == y:
                self.player_1.isDead = True
            if self.tiles[i, y] == const.WOOD:
                self.tiles[i, y] = const.EXPLOSION
                break
            if self.tiles[i, y] != const.WALL:
                self.tiles[i, y] = const.EXPLOSION
            else:
                break

        for i in [y, y - 1, y - 2, y - 3, y - 4, y - 5]:
            if self.player_1.get_pos_x() == x and self.player_1.get_pos_y() == i:
                self.player_1.isDead = True
            if self.tiles[x, i] == const.WOOD:
                self.tiles[x, i] = const.EXPLOSION
                break
            if self.tiles[x, i] != const.WALL:
                self.tiles[x, i] = const.EXPLOSION
            else:
                break

        for i in [y + 1, y + 2, y + 3, y + 4, y + 5]:
            if self.player_1.get_pos_x() == x and self.player_1.get_pos_y() == i:
                self.player_1.isDead = True
            if self.tiles[x, i] == const.WOOD:
                self.tiles[x, i] = const.EXPLOSION
                break
            if self.tiles[x, i] != const.WALL:
                self.tiles[x, i] = const.EXPLOSION
            else:
                break

    def clear_explosion(self, x, y):
        """Czyszczenie efektu eksplozji bomby

            Args:
                x (int): Pozycja x początku eksplozji
                y (int): Pozycja y początku eksplozji

        """
        for i in [x, x - 1, x - 2, x - 3, x - 4, x - 5]:
            if self.tiles[i, y] == const.EXPLOSION:
                self.tiles[i, y] = const.GRASS

        for i in [x + 1, x + 2, x + 3, x + 4, x + 5]:
            if self.tiles[i, y] == const.EXPLOSION:
                self.tiles[i, y] = const.GRASS

        for i in [y, y - 1, y - 2, y - 3, y - 4, y - 5]:
            if self.tiles[x, i] == const.EXPLOSION:
                self.tiles[x, i] = const.GRASS

        for i in [y + 1, y + 2, y + 3, y + 4, y + 5]:
            if self.tiles[x, i] == const.EXPLOSION:
                self.tiles[x, i] = const.GRASS
