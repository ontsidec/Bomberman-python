

class Player(object):
    """Klasa obsługująca poszczególnych graczy."""
    def __init__(self, name, x, y):
        """Domyślne ustawienia klasy

            Args:
                name (string): Nazwa gracza
                x (int): Pozycja x gracza
                y (int): Pozycja y gracza

        """
        self.name = name
        self.pos_x = x
        self.pos_y = y
        self.bombs = 1
        self.isDead = False

    def move(self, x, y):
        """Przesunięcie gracza na daną pozycje

            Args:
                x (int): Przesuń gracza na pozycje x
                y (int): Przesuń gracza na pozycje y

        """
        self.pos_x = x
        self.pos_y = y

    def get_pos_x(self):
        """Zwraca aktualną pozycje gracza

            Returns:
                x (int): Zwraca x pozycje gracza

        """
        return self.pos_x

    def get_pos_y(self):
        """Zwraca aktualną pozycje gracza

            Returns:
                y (int): Zwraca y pozycje gracza

        """
        return self.pos_y

    def place_bomb(self):
        """Stawianie bomby na pozycji gracza

            Returns:
                True - zwraca pozycje bomby jeżeli postawiono
                False - zwraca pozycje 0,0 czyli błędną

        """
        if self.bombs >= 1:
            self.bombs -= 1
            return self.pos_x, self.pos_y
        else:
            return 0, 0

    def give_bomb(self):
        """Daje graczowi bombę"""
        self.bombs += 1
