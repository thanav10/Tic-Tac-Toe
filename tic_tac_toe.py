import os
# cd ~/Desktop
# python3 tic_tac_toe.py
# --------- Global Variables -----------
board = ["1", "2", "3",
         "4", "5", "6",
         "7", "8", "9"]
game_still_going = True
winner = None
current_player = "X"

# ------------- Functions ---------------

def play_game():
    display_board()
    while game_still_going:
        handle_turn(current_player)
        check_if_game_over()
        if game_still_going:
            flip_player()
    if winner == "X" or winner == "O":
        print(winner + " won.")
    elif winner is None:
        print("Tie.")

def display_board():
    clear_screen()
    print("\n")
    print("  ———" + " ——— "+ "———  ")
    print(" | " + colorize(board[0]) + " | " + colorize(board[1]) + " | " + colorize(board[2] + " | "))
    print("  ———" + " ——— "+ "———  ")
    print(" | " + colorize(board[3]) + " | " + colorize(board[4]) + " | " + colorize(board[5] + " | "))
    print("  ———" + " ——— "+ "———  ")
    print(" | " + colorize(board[6]) + " | " + colorize(board[7]) + " | " + colorize(board[8] + " | "))
    print("  ———" + " ——— "+ "———  ")
    print("\n")

def handle_turn(player):
    print(player + "'s turn.")
    position = input("Choose a position from 1-9: ")
    valid = False
    while not valid:
        while position not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            position = input("Choose a position from 1-9: ")
        position = int(position) - 1
        if board[position] in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            valid = True
        else:
            print("You can't go there. Go again.")
            position = input("Choose a position from 1-9: ")

    board[position] = player
    display_board()

def check_if_game_over():
    check_for_winner()
    check_for_tie()

def check_for_winner():
    global winner
    row_winner = check_rows()
    column_winner = check_columns()
    diagonal_winner = check_diagonals()
    if row_winner:
        winner = row_winner
    elif column_winner:
        winner = column_winner
    elif diagonal_winner:
        winner = diagonal_winner
    else:
        winner = None

def check_rows():
    global game_still_going
    row_1 = board[0] == board[1] == board[2]
    row_2 = board[3] == board[4] == board[5]
    row_3 = board[6] == board[7] == board[8]
    if row_1 or row_2 or row_3:
        game_still_going = False
    if row_1:
        return board[0]
    elif row_2:
        return board[3]
    elif row_3:
        return board[6]
    else:
        return None

def check_columns():
    global game_still_going
    column_1 = board[0] == board[3] == board[6]
    column_2 = board[1] == board[4] == board[7]
    column_3 = board[2] == board[5] == board[8]
    if column_1 or column_2 or column_3:
        game_still_going = False
    if column_1:
        return board[0]
    elif column_2:
        return board[1]
    elif column_3:
        return board[2]
    else:
        return None

def check_diagonals():
    global game_still_going
    diagonal_1 = board[0] == board[4] == board[8]
    diagonal_2 = board[2] == board[4] == board[6]
    if diagonal_1 or diagonal_2:
        game_still_going = False
    if diagonal_1:
        return board[0]
    elif diagonal_2:
        return board[2]
    else:
        return None

def check_for_tie():
    global game_still_going
    if all(space in ["X", "O"] for space in board):
        game_still_going = False
        return True
    return False

def flip_player():
    global current_player
    current_player = "O" if current_player == "X" else "X"

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def colorize(symbol):
    if symbol == "X":
        return f"\033[91mX\033[0m"  # Red
    elif symbol == "O":
        return f"\033[94mO\033[0m"  # Blue
    else:
        return symbol

# ------------ Start Execution -------------
play_game()
