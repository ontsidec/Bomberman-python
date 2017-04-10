import board
import player

board = board.Board(21, 21, 2)

# Test bomby
board.display()
board.place_bomb(3, 2)
board.display()
board.explode(3, 2)
board.display()
"""
player_1 = player.Player("Gracz 1", 1, 1)
# board.display() # Do testów
while True:
    key = input()
    x = player_1.get_pos_x()
    y = player_1.get_pos_y()

    if key == 'w':
        print('Naciśnięto klawisz: w')
        if board.check_move(x, y - 1):
            player_1.move(x, y - 1)
    elif key == 's':
        print('Naciśnięto klawisz: s')
        if board.check_move(x, y + 1):
            player_1.move(x, y + 1)
    elif key == 'a':
        print('Naciśnięto klawisz: a')
        if board.check_move(x - 1, y):
            player_1.move(x - 1, y)
    elif key == 'd':
        print('Naciśnięto klawisz: d')
        if board.check_move(x + 1, y):
            player_1.move(x + 1, y)
    elif key == 'f':
        print('Naciśnięto klawisz: f')
        x, y = player_1.place_bomb()
        print(x, y)

    print(player_1.get_pos_x(), player_1.get_pos_y())
"""