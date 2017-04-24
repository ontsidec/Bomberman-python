from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QPixmap

from src import constants as const
from src import board

# noinspection PyArgumentList


class Game(QWidget):
    """Klasa obsługująca mechanikę gry"""
    def __init__(self, players):
        """Domyślne ustawienia klasy

            Args:
                players (int): Ilość wszystkich graczy

        """
        super(Game, self).__init__()

        self.startButton = QPushButton('New Game', self)
        self.startButton.setGeometry(720, 120, 120, 50)

        self.board = board.Board(players)
        self.timers = []
        self.timer = QTimer()
        self.timer.setInterval(const.GAME_SPEED)
        self.timer.timeout.connect(self.repaint)
        self.timer.start()
        self.show()

    def paintEvent(self, event):
        """Obsługa rysowania na ekranie"""
        painter = QPainter()
        painter.begin(self)
        self.draw_board(painter)
        painter.end()

    def draw_board(self, painter):
        """Wyświetlenie planszy na ekranie"""
        width = const.TILE_WIDTH
        height = const.TILE_HEIGHT

        for x in range(const.BOARD_WIDTH):
            for y in range(const.BOARD_HEIGHT):
                pos_x = x * width
                pos_y = y * height

                if self.board.tiles[x, y] == 0:  # wall
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/wall.png'))
                elif self.board.tiles[x, y] == 1:  # grass
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/grass.png'))
                elif self.board.tiles[x, y] == 2:  # brick
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/brick.png'))
                elif self.board.tiles[x, y] == 3:  # player
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/player.png'))
                elif self.board.tiles[x, y] == 4:  # bomb
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/bomb.png'))
                elif self.board.tiles[x, y] == 5:  # explosion
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/explosion.png'))
                else:  # wall
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/wall.png'))

    def keyPressEvent(self, event):
        """Obsługa klawiatury"""
        if not self.board.player_1.isDead:
            x = self.board.player_1.get_pos_x()
            y = self.board.player_1.get_pos_y()

            if event.key() == Qt.Key_W:
                if self.board.try_move(x, y - 1):
                    self.board.move(x, y - 1)
            elif event.key() == Qt.Key_S:
                if self.board.try_move(x, y + 1):
                    self.board.move(x, y + 1)
            elif event.key() == Qt.Key_A:
                if self.board.try_move(x - 1, y):
                    self.board.move(x - 1, y)
            elif event.key() == Qt.Key_D:
                if self.board.try_move(x + 1, y):
                    self.board.move(x + 1, y)
            elif event.key() == Qt.Key_F:
                x, y = self.board.player_1.place_bomb()
                if x != 0 and y != 0:
                    self.board.place_bomb(x, y)
                    self.timers.append(QTimer())
                    self.timers[len(self.timers) - 1].setInterval(const.BOMB_SPEED)
                    timer = self.timers[len(self.timers) - 1]
                    timer.timeout.connect(lambda: self.explode(x, y))
                    timer.timeout.connect(timer.stop)
                    timer.start()

    def explode(self, x, y):
        """Przesunięcie gracza na daną pozycje

            Args:
                x (int): Pozycja x bomby
                y (int): Pozycja y bomby

        """
        self.board.explode(x, y)
        self.board.player_1.give_bomb()
        self.timers.append(QTimer())
        self.timers[len(self.timers) - 1].setInterval(const.EXPLOSION_SPEED)
        timer = self.timers[len(self.timers) - 1]
        timer.timeout.connect(lambda: self.board.clear_explosion(x, y))
        timer.timeout.connect(timer.stop)
        timer.start()
