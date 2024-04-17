import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
ORIGINAL_WIDTH, ORIGINAL_HEIGHT = 800, 500
SCALE_FACTOR = 1.5
WIDTH, HEIGHT = int(ORIGINAL_WIDTH * SCALE_FACTOR), int(ORIGINAL_HEIGHT * SCALE_FACTOR)
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = int(WIDTH / 15), 20
BRICK_ROWS = 6  # Increased for the top bricks
BRICK_COLS = int(WIDTH / BRICK_WIDTH) - 1
BRICK_SPACING = 5
BRICK_OFFSET_TOP = 50
GAME_OVER_FONT_SIZE = 36

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Paddle
paddle_width = int(PADDLE_WIDTH * 2)  # Doubled the width
paddle_x = int((WIDTH - paddle_width) // 2)
paddle_y = int(HEIGHT - PADDLE_HEIGHT - 10)
paddle_speed = int(5 * SCALE_FACTOR)  # Doubled the speed

# Ball
ball_x = int(WIDTH // 2)
ball_y = int(HEIGHT // 2)
ball_dx = 0
ball_dy = 0

# Bricks
bricks = []
brick_width = BRICK_WIDTH
brick_cols = BRICK_COLS
if brick_width * BRICK_COLS + BRICK_SPACING * (BRICK_COLS - 1) > WIDTH:
    brick_width = (WIDTH - BRICK_SPACING * (BRICK_COLS - 1)) // BRICK_COLS
    brick_cols = BRICK_COLS

for i in range(BRICK_ROWS):
    for j in range(brick_cols):
        brick_x = j * (brick_width + BRICK_SPACING)
        brick_y = i * (BRICK_HEIGHT + BRICK_SPACING) + BRICK_OFFSET_TOP
        bricks.append(pygame.Rect(brick_x, brick_y, brick_width, BRICK_HEIGHT))

# Add top bricks
top_bricks = []
for i in range(brick_cols):
    brick_x = i * (brick_width + BRICK_SPACING)
    brick_y = BRICK_OFFSET_TOP - BRICK_HEIGHT - BRICK_SPACING
    top_bricks.append(pygame.Rect(brick_x, brick_y, brick_width, BRICK_HEIGHT))

# Game state
game_over = True

# Ball speed (default value)
ball_speed = int(1.25 * SCALE_FACTOR)  # Reduced by half

# Game over message
font = pygame.font.Font(None, int(GAME_OVER_FONT_SIZE * SCALE_FACTOR))
game_over_text = font.render("Press Space to Start", True, WHITE)
game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Speed selection message
speed_text = font.render("Select Ball Speed (1-9):", True, WHITE)
speed_rect = speed_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - int(50 * SCALE_FACTOR)))

# Speed selection
selected_speed = None

# Control pad speed factor
control_speed_factor = 0.5  # Doubled the speed

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if game_over:
        # Speed selection
        for i in range(1, 10):
            if keys[pygame.K_1 + i - 1]:
                selected_speed = i
                break

        if keys[pygame.K_SPACE] and selected_speed is not None:
            game_over = False
            ball_dx = random.choice([-1, 1]) * (selected_speed // 2)  # Reduced by 2x
            ball_dy = -(selected_speed // 2)  # Reduced by 2x
            bricks = [pygame.Rect(brick_x, brick_y, brick_width, BRICK_HEIGHT) for brick_x, brick_y in
                      [(j * (brick_width + BRICK_SPACING), i * (BRICK_HEIGHT + BRICK_SPACING) + BRICK_OFFSET_TOP) for i
                       in range(BRICK_ROWS) for j in range(brick_cols)]]
    else:
        # Move the paddle
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= int(paddle_speed * control_speed_factor)  # Doubled the speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
            paddle_x += int(paddle_speed * control_speed_factor)  # Doubled the speed

        # Move the ball
        ball_x += ball_dx
        ball_y += ball_dy

        # Collision with walls
        if ball_x < 0 or ball_x > WIDTH:
            ball_dx = -ball_dx
        if ball_y < 0:
            ball_dy = -ball_dy

        # Collision with paddle
        if (
            paddle_x < ball_x < paddle_x + paddle_width
            and paddle_y < ball_y < paddle_y + PADDLE_HEIGHT
        ):
            ball_dy = -ball_dy

        # Collision with bricks
        for brick in bricks.copy():
            if brick.colliderect(
                (ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, 2 * BALL_RADIUS, 2 * BALL_RADIUS)
            ):
                bricks.remove(brick)
                ball_dy = -ball_dy

        # Check if the ball is out of bounds
        if ball_y > HEIGHT:
            game_over = True

    # Clear the screen
    screen.fill(BLACK)

    # Draw the paddle
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, PADDLE_HEIGHT))

    # Draw the ball
    pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_RADIUS)

    # Draw the bricks
    for brick in bricks:
        pygame.draw.rect(screen, WHITE, brick)

    # Draw the top bricks
    for brick in top_bricks:
        pygame.draw.rect(screen, WHITE, brick)

    # Draw game over text if the game is over
    if game_over:
        screen.blit(game_over_text, game_over_rect)
        screen.blit(speed_text, speed_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
