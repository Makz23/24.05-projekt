import pygame
import random

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

white = (255, 255, 255)
black = (0, 0, 0)

paddle_width = 10
paddle_height = 100

ball_size = 10

paddle_speed = 10

ball_speed_x = 6
ball_speed_y = 6


player_paddle = pygame.Rect(50, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)
ai_paddle = pygame.Rect(screen_width - 50 - paddle_width, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)


ball = pygame.Rect(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, ball_size, ball_size)


player_score = 0
ai_score = 0


font = pygame.font.Font(None, 74)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.y -= paddle_speed
    if keys[pygame.K_s] and player_paddle.bottom < screen_height:
        player_paddle.y += paddle_speed

    if ai_paddle.top < ball.y:
        ai_paddle.y += paddle_speed
    if ai_paddle.bottom > ball.y:
        ai_paddle.y -= paddle_speed

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.colliderect(player_paddle) or ball.colliderect(ai_paddle):
        ball_speed_x *= -1

    if ball.left <= 0:
        ai_score += 1
        ball = pygame.Rect(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, ball_size, ball_size)
        ball_speed_x *= random.choice([-1, 1])
        ball_speed_y *= random.choice([-1, 1])
    if ball.right >= screen_width:
        player_score += 1
        ball = pygame.Rect(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, ball_size, ball_size)
        ball_speed_x *= random.choice([-1, 1])
        ball_speed_y *= random.choice([-1, 1])

    screen.fill(black)
    pygame.draw.rect(screen, white, player_paddle)
    pygame.draw.rect(screen, white, ai_paddle)
    pygame.draw.ellipse(screen, white, ball)
    pygame.draw.aaline(screen, white, (screen_width // 2, 0), (screen_width // 2, screen_height))

    player_text = font.render(str(player_score), True, white)
    screen.blit(player_text, (screen_width // 2 - 100, 10))
    ai_text = font.render(str(ai_score), True, white)
    screen.blit(ai_text, (screen_width // 2 + 50, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
