import pygame
import random
import os

# Constants
WIDTH, HEIGHT = 960, 720
WHITE = (255, 255, 255)
BG_COLOR = (20, 20, 20)
BALL_COLOR = (0, 200, 255)
PADDLE_COLOR = (255, 100, 255)

def show_point(screen, font, msg_font, message):
    screen.fill(BG_COLOR)
    title = font.render(message, True, WHITE)
    note = msg_font.render("Next round in 2 seconds...", True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))
    screen.blit(note, note.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))
    pygame.display.flip()
    pygame.time.delay(2000)

def reset_positions(ball, p1, p2):
    ball.center = (WIDTH // 2, HEIGHT // 2)
    p1.centery = HEIGHT // 2
    p2.centery = HEIGHT // 2

def pong():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong Showdown")
    clock = pygame.time.Clock()

    font_main = pygame.font.SysFont("Consolas", 42, bold=True)
    font_small = pygame.font.SysFont("Consolas", 28)

    sound_file = os.path.join(os.path.dirname(__file__), "hit.wav")
    bounce_sound = pygame.mixer.Sound(sound_file) if os.path.isfile(sound_file) else None

    # Game state
    running = False
    score_1 = 0
    score_2 = 0

    # Game objects
    paddle_left = pygame.Rect(30, HEIGHT // 2 - 50, 7, 100)
    paddle_right = pygame.Rect(WIDTH - 50, HEIGHT // 2 - 50, 7, 100)
    move_left = 0
    move_right = 0

    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 25, 25)
    speed_x = random.choice([-1, 1]) * random.uniform(0.2, 0.4)
    speed_y = random.choice([-1, 1]) * random.uniform(0.2, 0.4)

    def new_ball_speed():
        nonlocal speed_x, speed_y
        speed_x = random.choice([-1, 1]) * random.uniform(0.2, 0.4)
        speed_y = random.choice([-1, 1]) * random.uniform(0.2, 0.4)

    while True:
        screen.fill(BG_COLOR)

        if not running:
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                start_msg = font_small.render("Press SPACE to Play", True, WHITE)
                screen.blit(start_msg, start_msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            pygame.display.flip()
            clock.tick(60)
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    return
                if evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE:
                    running = True
            continue

        dt = clock.tick(60)

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                return
            elif evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_w: move_left = -0.5
                elif evt.key == pygame.K_s: move_left = 0.5
                elif evt.key == pygame.K_UP: move_right = -0.5
                elif evt.key == pygame.K_DOWN: move_right = 0.5
            elif evt.type == pygame.KEYUP:
                if evt.key in [pygame.K_w, pygame.K_s]: move_left = 0
                if evt.key in [pygame.K_UP, pygame.K_DOWN]: move_right = 0

        # Move paddles
        paddle_left.y += move_left * dt
        paddle_right.y += move_right * dt
        paddle_left.clamp_ip(screen.get_rect())
        paddle_right.clamp_ip(screen.get_rect())

        # Bounce off top and bottom
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            speed_y *= -1
            if bounce_sound: bounce_sound.play()

        # Checking for scores
        if ball.left <= 0:
            score_2 += 1
            show_point(screen, font_main, font_small, "Player 2 Scores!")
            reset_positions(ball, paddle_left, paddle_right)
            new_ball_speed()
            running = False
            continue

        if ball.right >= WIDTH:
            score_1 += 1
            show_point(screen, font_main, font_small, "Player 1 Scores!")
            reset_positions(ball, paddle_left, paddle_right)
            new_ball_speed()
            running = False
            continue

        # Paddle collision
        if paddle_left.colliderect(ball) and ball.left > paddle_left.left:
            speed_x *= -1.1
            ball.left = paddle_left.right
            if bounce_sound: bounce_sound.play()
        if paddle_right.colliderect(ball) and ball.right < paddle_right.right:
            speed_x *= -1.1
            ball.right = paddle_right.left
            if bounce_sound: bounce_sound.play()

        # Ball movement
        ball.x += speed_x * dt
        ball.y += speed_y * dt

        # Drawing
        pygame.draw.rect(screen, PADDLE_COLOR, paddle_left, border_radius=6)
        pygame.draw.rect(screen, PADDLE_COLOR, paddle_right, border_radius=6)
        pygame.draw.ellipse(screen, BALL_COLOR, ball)

        score_display = font_main.render(f"{score_1}    {score_2}", True, WHITE)
        screen.blit(score_display, (WIDTH // 2 - score_display.get_width() // 2, 20))

        pygame.display.update()

if __name__ == "__main__":
    pong()

