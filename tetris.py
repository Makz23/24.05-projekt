import pygame
import random


pygame.init()


screen_width = 300
screen_height = 600
block_size = 30
screen = pygame.display.set_mode((screen_width, screen_height))


colors = [
    (0, 0, 0),
    (255, 85, 85),
    (100, 200, 115),
    (120, 108, 245),
    (255, 140, 50),
    (50, 120, 52),
    (146, 202, 73),
    (150, 161, 218),
]

background_colors = [
    (0, 0, 0),
    (30, 30, 30),
    (60, 60, 60),
    (90, 90, 90),
    (120, 120, 120),
    (150, 150, 150),
]


shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[0, 1, 0], [1, 1, 1]]
]

cols = screen_width // block_size
rows = screen_height // block_size

grid = [[0 for _ in range(cols)] for _ in range(rows)]

def rotate(shape):
    return [ [ shape[y][x]
            for y in range(len(shape)) ]
            for x in range(len(shape[0]) - 1, -1, -1) ]

class Tetrimino:
    def __init__(self, shape):
        self.shape = shape
        self.color = colors[shapes.index(shape) + 1]
        self.x = cols // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = rotate(self.shape)

    def intersects(self, grid):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell and (
                        x + self.x < 0 or
                        x + self.x >= cols or
                        y + self.y >= rows or
                        grid[y + self.y][x + self.x]):
                    return True
        return False

    def place(self, grid):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid[y + self.y][x + self.x] = self.color

def new_tetrimino():
    return Tetrimino(random.choice(shapes))

def check_lines(grid):
    lines = 0
    for y in range(rows):
        if all(grid[y]):
            del grid[y]
            grid.insert(0, [0 for _ in range(cols)])
            lines += 1
    return lines

def draw_grid(screen, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            pygame.draw.rect(screen, cell, pygame.Rect(x * block_size, y * block_size, block_size, block_size))
            pygame.draw.rect(screen, (40, 40, 40), pygame.Rect(x * block_size, y * block_size, block_size, block_size), 1)
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, screen_width, screen_height), 5)

def draw_score(screen, score, level, lines):
    font = pygame.font.SysFont('Arial', 24)
    score_surf = font.render(f'Score: {score}', True, (255, 255, 255))
    level_surf = font.render(f'Level: {level}', True, (255, 255, 255))
    lines_surf = font.render(f'Lines: {lines}', True, (255, 255, 255))
    screen.blit(score_surf, (10, 10))
    screen.blit(level_surf, (10, 40))
    screen.blit(lines_surf, (10, 70))

def draw_preview(screen, grid, tetrimino):
    temp_y = tetrimino.y
    while not tetrimino.intersects(grid):
        tetrimino.y += 1
    tetrimino.y -= 1
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, (200, 200, 200), pygame.Rect((tetrimino.x + x) * block_size, (tetrimino.y + y) * block_size, block_size, block_size), 1)
    tetrimino.y = temp_y




def main():
    clock = pygame.time.Clock()
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    tetrimino = new_tetrimino()
    next_tetrimino = new_tetrimino()
    fall_time = 0
    fall_speed = 0.25
    score = 0
    level = 1
    lines_cleared = 0
    max_lines = 9999
    paused = False
    color_index = 0

    line_clear_sound = pygame.mixer.Sound('line_clear.mp3')
    piece_place_sound = pygame.mixer.Sound('block_place.mp3')

    def reset_game():
        nonlocal grid, clock, tetrimino, next_tetrimino, fall_time, fall_speed, score, level, lines_cleared, paused, color_index, running
        tetrimino = new_tetrimino()
        next_tetrimino = new_tetrimino()
        fall_time = 0
        fall_speed = 0.25
        score = 0
        level = 1
        lines_cleared = 0
        paused = False
        color_index = 0
        running = True

    running = True
    while running:
        grid_copy = [row[:] for row in grid]
        fall_time += clock.get_rawtime()
        clock.tick()

        if not paused:
            if fall_time / 1000 >= fall_speed:
                fall_time = 0
                tetrimino.y += 1
                if tetrimino.intersects(grid):
                    tetrimino.y -= 1
                    tetrimino.place(grid)
                    piece_place_sound.play()
                    lines = check_lines(grid)
                    score += lines * 100 * lines
                    lines_cleared += lines
                    if lines > 0:
                        line_clear_sound.play()
                    if lines_cleared >= level * 3:
                        level += 1
                        color_index = (color_index + 1) % len(background_colors)
                        fall_speed = max(0.1, fall_speed - 0.05)
                    if lines_cleared >= max_lines:
                        running = False
                    tetrimino = next_tetrimino
                    next_tetrimino = new_tetrimino()
                    if tetrimino.intersects(grid):
                        running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        tetrimino.x -= 1
                        if tetrimino.intersects(grid):
                            tetrimino.x += 1
                    if event.key == pygame.K_RIGHT:
                        tetrimino.x += 1
                        if tetrimino.intersects(grid):
                            tetrimino.x -= 1
                    if event.key == pygame.K_DOWN:
                        tetrimino.y += 1
                        if tetrimino.intersects(grid):
                            tetrimino.y -= 1
                    if event.key == pygame.K_UP:
                        tetrimino.rotate()
                        if tetrimino.intersects(grid):
                            tetrimino.rotate()
                            tetrimino.rotate()
                            tetrimino.rotate()
                    if event.key == pygame.K_SPACE:
                        while not tetrimino.intersects(grid):
                            tetrimino.y += 1
                        tetrimino.y -= 1
                    if event.key == pygame.K_p:
                        paused = not paused

        screen.fill(background_colors[color_index])
        draw_grid(screen, grid_copy)
        for y, row in enumerate(tetrimino.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, tetrimino.color, pygame.Rect((tetrimino.x + x) * block_size, (tetrimino.y + y) * block_size, block_size, block_size))

        draw_preview(screen, grid, tetrimino)
        draw_score(screen, score, level, lines_cleared)

        pygame.display.flip()

    # Game Over prompt
    game_over_font = pygame.font.SysFont('Arial', 36)
    game_over_surf = game_over_font.render('Game Over', True, (255, 255, 255))
    prompt_surf = game_over_font.render('Press Q to Quit or C to Play Again', True, (255, 255, 255))
    screen.blit(game_over_surf, (screen_width // 2 - game_over_surf.get_width() // 2, screen_height // 2 - game_over_surf.get_height() // 2 - 50))
    screen.blit(prompt_surf, (screen_width // 2 - prompt_surf.get_width() // 2, screen_height // 2 - prompt_surf.get_height() // 2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    waiting = False
                if event.key == pygame.K_c:
                    main()
                    reset_game()

    pygame.quit()

if __name__ == "__main__":
    main()

