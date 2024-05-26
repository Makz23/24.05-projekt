import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 400, 400
ROWS, COLS = 10, 10
MINES = 15
SQUARE_SIZE = WIDTH // COLS
FONT = pygame.font.SysFont('arial', 24)

BG_COLOR = (255, 255, 255)
GRID_COLOR = (0, 0, 0)
MINE_COLOR = (255, 0, 0)
TEXT_COLOR = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Minesweeper')

board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
mines = set()

def place_mines():
    while len(mines) < MINES:
        x = random.randint(0, ROWS - 1)
        y = random.randint(0, COLS - 1)
        if (x, y) not in mines:
            mines.add((x, y))
            board[x][y] = -1
            for i in range(max(0, x-1), min(ROWS, x+2)):
                for j in range(max(0, y-1), min(COLS, y+2)):
                    if board[i][j] != -1:
                        board[i][j] += 1

def draw_board(revealed):
    screen.fill(BG_COLOR)
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)
            if revealed[row][col]:
                if board[row][col] == -1:
                    pygame.draw.circle(screen, MINE_COLOR, rect.center, SQUARE_SIZE // 4)
                elif board[row][col] > 0:
                    text_surface = FONT.render(str(board[row][col]), True, TEXT_COLOR)
                    screen.blit(text_surface, (col * SQUARE_SIZE + SQUARE_SIZE // 3, row * SQUARE_SIZE + SQUARE_SIZE // 4))

def reveal_board(revealed):
    for row in range(ROWS):
        for col in range(COLS):
            revealed[row][col] = True

def reveal_cell(revealed, row, col):
    if revealed[row][col]:
        return
    revealed[row][col] = True
    if board[row][col] == 0:
        for i in range(max(0, row-1), min(ROWS, row+2)):
            for j in range(max(0, col-1), min(COLS, col+2)):
                if not revealed[i][j]:
                    reveal_cell(revealed, i, j)

def main():
    place_mines()
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    game_over = False
    win = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX, mouseY = event.pos
                clicked_row = mouseX // SQUARE_SIZE
                clicked_col = mouseY // SQUARE_SIZE

                if (clicked_row, clicked_col) in mines:
                    reveal_board(revealed)
                    game_over = True
                    win = False
                else:
                    reveal_cell(revealed, clicked_row, clicked_col)
                    if all(revealed[row][col] or (row, col) in mines for row in range(ROWS) for col in range(COLS)):
                        game_over = True
                        win = True

        draw_board(revealed)
        pygame.display.update()

        if game_over:
            if win:
                print("Congratulations! You've cleared the minefield.")
            else:
                print("Game Over! You hit a mine.")
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
