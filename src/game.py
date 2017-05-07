from PyQt5.QtWidgets import QWidget, qApp
from PyQt5.QtCore import QTimer, Qt, QEvent
from PyQt5.QtGui import QPainter, QPixmap

import xml.dom.minidom as xml
import numpy as np

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
        qApp.installEventFilter(self)
        self.released = True
        self.players = players

        self.board = board.Board(players)
        self.timers = []
        self.timer = QTimer()
        self.timer.setInterval(const.GAME_SPEED)
        self.timer.timeout.connect(self.repaint)
        self.timer.start()

        self.nr_frame = 0
        if self.players != 0:
            self.frames = []
            self.frame = np.ones((const.BOARD_WIDTH, const.BOARD_HEIGHT), dtype=int)
            self.doc = xml.Document()
            self.root = self.doc.createElement('save')
        else:
            doc = xml.parse("autosave.xml")
            self.frames = doc.getElementsByTagName("frame")

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

        self.nr_frame += 1
        if self.players == 0:
            self.get_from_xml()

        for x in range(const.BOARD_WIDTH):
            for y in range(const.BOARD_HEIGHT):
                pos_x = x * width
                pos_y = y * height

                if self.board.tiles[x, y] == const.WALL:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/wall.png'))
                elif self.board.tiles[x, y] == const.GRASS:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/grass.png'))
                elif self.board.tiles[x, y] == const.WOOD:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/wood.png'))
                elif self.board.tiles[x, y] == const.PLAYER_FRONT:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/player_front.png'))
                elif self.board.tiles[x, y] == const.BOMB:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/bomb.png'))
                elif self.board.tiles[x, y] == const.EXPLOSION:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/explosion.png'))
                else:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/wall.png'))

        if self.players != 0:
            self.check_changes()

    def eventFilter(self, obj, event):
        """Obsługa klawiatury"""
        if event.type() == QEvent.KeyRelease:
            self.released = True

        if event.type() == QEvent.KeyPress and self.released and self.players != 0:
            self.released = False
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

        return super(Game, self).eventFilter(obj, event)

    def explode(self, x, y):
        """Wybuch bomby

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

    def check_changes(self):
        """Sprawdzenie czy klatki się różnią"""
        if not np.array_equal(self.frame, self.board.tiles):
            self.board.save_change(self.frame)
            self.frame = np.copy(self.board.tiles)
            self.frames.append(self.nr_frame)

        if self.board.player_1.isDead:
            self.save_xml()

    def save_xml(self):
        """Zapisywanie rozgrywki do dokumentu XML"""
        i = 0
        element = self.board.board_history[i]
        for nr_frame in self.frames:
            frame = self.doc.createElement("frame")
            frame.setAttribute("id", str(nr_frame))
            self.root.appendChild(frame)
            moves = []
            while element != '#':
                moves.append(element)
                i += 1
                element = self.board.board_history[i]

            line = self.doc.createTextNode(str(moves))
            frame.appendChild(line)
            if i < len(self.board.board_history) - 1:
                i += 1
                element = self.board.board_history[i]

        self.doc.appendChild(self.root)
        self.doc.writexml(open('autosave.xml', 'w'), indent="  ", addindent="  ", newl='\n')
        self.doc.unlink()

    def get_from_xml(self):
        for frame in self.frames:
            if int(frame.getAttribute("id")) == self.nr_frame:
                line = frame.firstChild.data
                ignore = True
                selected = 0
                x = ""
                y = ""
                value = ""
                for char in line:
                    if char == "!":
                        ignore = True
                    if char == "@":
                        ignore = False
                    if not ignore:
                        if char == '*':
                            if selected == 2:
                                selected = 0
                                self.board.tiles[int(x), int(y)] = int(value)
                                x = ""
                                y = ""
                                value = ""
                            else:
                                selected += 1
                        else:
                            if char != '@':
                                if selected == 0:
                                    x += char
                                if selected == 1:
                                    y += char
                                if selected == 2:
                                    value += char
