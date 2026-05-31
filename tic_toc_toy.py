import math


board = [" " for _ in range(9)]


def print_board():
    print("\n")
    for i in range(0, 9, 3):
        print(f" {board[i]} | {board[i+1]} | {board[i+2]} ")
        if i < 6:
            print("---|---|---")
    print("\n")


def check_winner(player):
    win_combinations = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]

    for combo in win_combinations:
        if all(board[pos] == player for pos in combo):
            return True
    return False


def is_draw():
    return " " not in board


def minimax(is_maximizing):
    if check_winner("O"):
        return 1
    if check_winner("X"):
        return -1
    if is_draw():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score

    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score


def ai_move():
    best_score = -math.inf
    move = -1

    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(False)
            board[i] = " "

            if score > best_score:
                best_score = score
                move = i

    board[move] = "O"


def human_move():
    while True:
        try:
            move = int(input("Enter position (1-9): ")) - 1

            if 0 <= move <= 8 and board[move] == " ":
                board[move] = "X"
                break
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Please enter a number between 1 and 9.")


print("Welcome to Tic-Tac-Toe!")
print("Positions:")
print("1 | 2 | 3")
print("4 | 5 | 6")
print("7 | 8 | 9")

while True:
    print_board()

    human_move()

    if check_winner("X"):
        print_board()
        print("You Win!")
        break

    if is_draw():
        print_board()
        print("It's a Draw!")
        break

    ai_move()

    if check_winner("O"):
        print_board()
        print("AI Wins!")
        break

    if is_draw():
        print_board()
        print("It's a Draw!")
        break
