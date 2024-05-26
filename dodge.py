import pygame
import random


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 50  
CAR_SIZE = GRID_SIZE
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge")
clock = pygame.time.Clock()

class Car:
    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.image = pygame.Surface((CAR_SIZE, CAR_SIZE))
        self.image.fill(RED)

    def move_left(self):
        if self.grid_x > 0:
            self.grid_x -= 1

    def move_right(self):
        if self.grid_x < GRID_WIDTH - 1:
            self.grid_x += 1

    def draw(self, screen):
        screen.blit(self.image, (self.grid_x * GRID_SIZE, self.grid_y * GRID_SIZE))

class Obstacle:
    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.image = pygame.Surface((CAR_SIZE, CAR_SIZE))
        self.image.fill(GREEN)

    def update(self):
        self.grid_y += 1
        if self.grid_y >= GRID_HEIGHT:
            self.grid_y = 0
            self.grid_x = random.randint(0, GRID_WIDTH - 1)

    def draw(self, screen):
        screen.blit(self.image, (self.grid_x * GRID_SIZE, self.grid_y * GRID_SIZE))

def main():
    running = True
    car = Car(GRID_WIDTH // 2, GRID_HEIGHT - 2)
    obstacles = [Obstacle(random.randint(0, GRID_WIDTH - 1), random.randint(-GRID_HEIGHT, 0)) for _ in range(5)]
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car.move_left()
        if keys[pygame.K_RIGHT]:
            car.move_right()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            car.move_left()
        if keys[pygame.K_d]:
            car.move_right()

        screen.fill(BLACK)

        car.draw(screen)
        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw(screen)
            if car.grid_x == obstacle.grid_x and car.grid_y == obstacle.grid_y:
                running = False

        pygame.display.flip()
        clock.tick(20)

    pygame.quit()

if __name__ == "__main__":
    main()

