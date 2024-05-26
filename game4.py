
import numpy as np

ROWS = 6
COLS = 7
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2

def create_board():
    return np.zeros((ROWS, COLS), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROWS-1][col] == EMPTY

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == EMPTY:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    for c in range(COLS-3):
        for r in range(ROWS):
            if all([board[r][c+i] == piece for i in range(4)]):
                return True
    for c in range(COLS):
        for r in range(ROWS-3):
            if all([board[r+i][c] == piece for i in range(4)]):
                return True
    for c in range(COLS-3):
        for r in range(ROWS-3):
            if all([board[r+i][c+i] == piece for i in range(4)]):
                return True
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if all([board[r-i][c+i] == piece for i in range(4)]):
                return True
    return False

def main():
    board = create_board()
    game_over = False
    turn = 0

    print_board(board)

    while not game_over:
        if turn == 0:
            col = int(input("Player 1, make your selection (0-6): "))
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER1)

                if winning_move(board, PLAYER1):
                    print("Player 1 wins!")
                    game_over = True
        else:
            col = int(input("Player 2, make your selection (0-6): "))
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER2)

                if winning_move(board, PLAYER2):
                    print("Player 2 wins!")
                    game_over = True

        print_board(board)

        turn += 1
        turn = turn % 2

if __name__ == "__main__":
    main()
