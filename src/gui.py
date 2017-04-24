from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5.QtGui import QIcon

from src import game
from src import constants as const

# noinspection PyArgumentList


class Window(QMainWindow):
    """Klasa obsługująca główne okno gry"""
    def __init__(self):
        """Domyślne ustawienia klasy"""
        super().__init__()

        self.game = game.Game(1)
        self.setCentralWidget(self.game)

        self.resize(const.BOARD_WIDTH * const.TILE_WIDTH, const.BOARD_HEIGHT * const.TILE_HEIGHT)
        self.center()
        self.setWindowTitle('Bomberman')
        self.setWindowIcon(QIcon('../res/images/bomb.png'))
        self.show()

    def center(self):
        """Wycentrowanie okna gry na ekranie"""
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
