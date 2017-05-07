from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QStackedWidget, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal

from src import game
from src import constants as const

import sys

# noinspection PyArgumentList


class Window(QMainWindow):
    """Klasa obsługująca główne okno gry"""
    def __init__(self):
        """Domyślne ustawienia klasy"""
        super().__init__()

        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainMenuWidget = MainMenu()
        self.game = game.Game(1)
        self.menu()

        self.setWindowTitle('Bomberman')
        self.setWindowIcon(QIcon('../res/images/icon.png'))
        self.show()

    def center(self):
        """Wycentrowanie okna gry na ekranie"""
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def menu(self):
        """Pokazanie menu głównego"""

        self.mainMenuWidget.playGameSignal.connect(self.play)
        self.mainMenuWidget.playReplaySignal.connect(self.replay)
        self.mainMenuWidget.quitGameSignal.connect(self.quit)

        self.centralWidget.addWidget(self.mainMenuWidget)
        self.centralWidget.setCurrentWidget(self.mainMenuWidget)

        self.resize(240, 250)
        self.center()

    def play(self):
        """Rozpoczęcie nowej gry"""

        self.setCentralWidget(self.game)
        self.resize(const.BOARD_WIDTH * const.TILE_WIDTH, const.BOARD_HEIGHT * const.TILE_HEIGHT)
        self.center()

    def replay(self):
        """Odtworzenie powtórki ostatniej gry"""

        self.game = game.Game(0)
        self.setCentralWidget(self.game)
        self.resize(const.BOARD_WIDTH * const.TILE_WIDTH, const.BOARD_HEIGHT * const.TILE_HEIGHT)
        self.center()

    @staticmethod
    def quit():
        sys.exit()

# noinspection PyArgumentList


class MainMenu(QWidget):

    playGameSignal = pyqtSignal()
    quitGameSignal = pyqtSignal()
    playReplaySignal = pyqtSignal()

    def __init__(self):
        super(MainMenu, self).__init__()

        button_width = 190
        button_height = 50
        button_offset = 25

        play_button = QPushButton('Graj', self)
        play_button.setFixedWidth(button_width)
        play_button.setFixedHeight(button_height)
        play_button.move(button_offset, (button_offset * 1) + (button_height * 0))
        play_button.clicked.connect(self.play)

        load_button = QPushButton('Odtwórz Powtórkę', self)
        load_button.setFixedWidth(button_width)
        load_button.setFixedHeight(button_height)
        load_button.move(button_offset, (button_offset * 2) + (button_height * 1))
        load_button.clicked.connect(self.load)

        quit_button = QPushButton('Wyjdź', self)
        quit_button.setFixedWidth(button_width)
        quit_button.setFixedHeight(button_height)
        quit_button.move(button_offset, (button_offset * 3) + (button_height * 2))
        quit_button.clicked.connect(self.quit)

        self.show()

    def play(self):
        """Emituje sygnał rozpoczęcia nowej gry"""
        self.playGameSignal.emit()

    def load(self):
        """Emituje sygnał wczytania powtórki ostatniej gry"""
        self.playReplaySignal.emit()

    def quit(self):
        """Emituje sygnał wyjścia z gry"""
        self.quitGameSignal.emit()
