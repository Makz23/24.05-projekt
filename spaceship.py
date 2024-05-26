import pygame
import random
import time

class GameObject:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Spaceship(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.speed = 5 
        self.bullets = []
        self.last_shot_time = 0
        self.shooting_delay = 200  
        self.power_up = None
        self.power_up_end_time = 0

    def move_left(self):
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self):
        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width

    def shoot(self, bullet_image):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shooting_delay:
            self.last_shot_time = current_time
            if self.power_up == 'triple_shot':
                self.bullets.append(Bullet(self.rect.centerx - 35, self.rect.top, bullet_image))
                self.bullets.append(Bullet(self.rect.centerx, self.rect.top, bullet_image))
                self.bullets.append(Bullet(self.rect.centerx + 35, self.rect.top, bullet_image))
            else:
                bullet = Bullet(self.rect.centerx, self.rect.top, bullet_image)
                self.bullets.append(bullet)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

    def draw(self, screen):
        super().draw(screen)
        for bullet in self.bullets:
            bullet.draw(screen)

    def apply_power_up(self, power_up_type, duration):
        self.power_up = power_up_type
        self.power_up_end_time = pygame.time.get_ticks() + duration

    def update_power_up(self):
        if self.power_up and pygame.time.get_ticks() > self.power_up_end_time:
            self.power_up = None
            self.speed = 5  

class Bullet(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed

class Asteroid(GameObject):
    def __init__(self, x, y, image, speed, points):
        super().__init__(x, y, image)
        self.speed = speed
        self.points = points

    def update(self):
        self.rect.y += self.speed

class PowerUp(GameObject):
    def __init__(self, x, y, image, type):
        super().__init__(x, y, image)
        self.type = type
        self.speed = 3

    def update(self):
        self.rect.y += self.speed

class Game:
    def __init__(self):
        self.spaceship_image = pygame.Surface((50, 50))
        self.spaceship_image.fill((0, 0, 255))
        self.bullet_image = pygame.Surface((5, 10))
        self.bullet_image.fill((255, 0, 0))
        self.asteroid_image = pygame.Surface((50, 50))
        self.asteroid_image.fill((128, 128, 128))
        self.red_asteroid_image = pygame.Surface((50, 50))
        self.red_asteroid_image.fill((255, 0, 0))
        self.power_up_image = pygame.Surface((30, 30))
        self.power_up_image.fill((0, 255, 0))

        self.reset_game()

    def reset_game(self):
        self.spaceship = Spaceship(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, self.spaceship_image)
        self.asteroids = [self.create_asteroid() for _ in range(5)]
        self.power_ups = []
        self.score = 0
        self.game_duration = 60000  # 1 minute
        self.game_end_time = pygame.time.get_ticks() + self.game_duration

    def create_asteroid(self):
        x = random.randint(0, SCREEN_WIDTH - 50)
        y = random.randint(-100, -50)
        speed = random.randint(2, 6)
        points = 10
        if random.random() < 0.2:  # 20% na czerwonego
            return Asteroid(x, y, self.red_asteroid_image, speed, 50)
        else:
            return Asteroid(x, y, self.asteroid_image, speed, points)

    def create_power_up(self):
        x = random.randint(0, SCREEN_WIDTH - 30)
        y = random.randint(-100, -50)
        power_up_type = random.choice(['triple_shot', 'destroy_all', 'speed_boost'])
        return PowerUp(x, y, self.power_up_image, power_up_type)

    def run(self):
        running = True
        while running:
            while self.run_game():
                pass
            running = self.show_end_screen()

        pygame.quit()
        print(f"Final Score: {self.score}")

    def run_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.spaceship.shoot(self.bullet_image)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.spaceship.move_left()
        if keys[pygame.K_RIGHT]:
            self.spaceship.move_right()

        screen.fill((0, 0, 0))
        
        self.spaceship.update_bullets()
        self.spaceship.update_power_up()
        self.spaceship.draw(screen)

        for asteroid in self.asteroids:
            asteroid.update()
            asteroid.draw(screen)
            if asteroid.rect.top > SCREEN_HEIGHT:
                self.asteroids.remove(asteroid)
                self.asteroids.append(self.create_asteroid())
            if self.spaceship.rect.colliderect(asteroid.rect):
                return False  
            for bullet in self.spaceship.bullets:
                if asteroid.rect.colliderect(bullet.rect):
                    self.spaceship.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)
                    self.asteroids.append(self.create_asteroid())
                    self.score += asteroid.points

        if random.random() < 0.01:  # Randomly create power-ups
            self.power_ups.append(self.create_power_up())

        for power_up in self.power_ups:
            power_up.update()
            power_up.draw(screen)
            if power_up.rect.top > SCREEN_HEIGHT:
                self.power_ups.remove(power_up)
            if self.spaceship.rect.colliderect(power_up.rect):
                if power_up.type == 'triple_shot':
                    self.spaceship.apply_power_up('triple_shot', 5000)
                elif power_up.type == 'destroy_all':
                    self.score += sum(asteroid.points for asteroid in self.asteroids)
                    self.asteroids = [self.create_asteroid() for _ in range(5)]
                elif power_up.type == 'speed_boost':
                    self.spaceship.speed = 10
                    self.spaceship.apply_power_up('speed_boost', 5000)
                self.power_ups.remove(power_up)

        if pygame.time.get_ticks() > self.game_end_time:
            return False  # End the game when time is up

        score_text = pygame.font.SysFont(None, 36).render(f'Score: {self.score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)
        
        return True

    def show_end_screen(self):
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 48)
        end_text = font.render(f'Game Over! Your Score: {self.score}', True, (255, 255, 255))
        prompt_text = font.render('Press Q to Quit or C to Play Again', True, (255, 255, 255))
        screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return False
                    if event.key == pygame.K_c:
                        self.reset_game()
                        return True
        return False

if __name__ == "__main__":
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Shooter")
    clock = pygame.time.Clock()

    game = Game()
    game.run()
 