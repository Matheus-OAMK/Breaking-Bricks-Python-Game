import pygame
from pygame.locals import *

pygame.init()
# Create the game window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakin' Bricks")

# Font
font = pygame.font.SysFont("Arial", 20)

# Score
score = 0

# Bat
bat = pygame.image.load("./images/paddle.png")
bat = bat.convert_alpha()
bat_rect = bat.get_rect()
# initial bat position
bat_rect.y = screen.get_height() - 100
bat_rect.x = (screen.get_width() - bat_rect.width) / 2

# Ball
ball = pygame.image.load("./images/football.png")
ball = ball.convert_alpha()
ball_rect = ball.get_rect()
ball_start = ((screen.get_width() - ball_rect.width) / 2, bat_rect.y - 35)
ball_speed = (3.0, 3.0)
ball_speed_increase = 1.1
ball_served = False
sx, sy = ball_speed
ball_rect.topleft = ball_start

# Brick
brick = pygame.image.load("./images/brick.png")
brick = brick.convert_alpha()
brick_rect = brick.get_rect()
brick_gap = 10
brick_rows = 5
brick_cols = screen.get_width() // (brick_rect.width + brick_gap)
side_gap = (
    screen.get_width() - (brick_rect.width + brick_gap) * brick_cols + brick_gap
) // 2


# **** Helper functions ****
# Function to create bricks
def create_bricks():
    global bricks
    bricks = []
    for y in range(brick_rows):
        brickY = y * (brick_rect.height + brick_gap)
        for x in range(brick_cols):
            brickX = x * (brick_rect.width + brick_gap) + side_gap
            bricks.append((brickX, brickY))


# Function to restart the game
def restart_game():
    global ball_served
    global sx, sy
    global score
    ball_served = False
    # Reset the ball
    ball_rect.topleft = ball_start
    # Reset the bat
    bat_rect.y = screen.get_height() - 100
    bat_rect.x = (screen.get_width() - bat_rect.width) / 2
    sx, sy = ball_speed  # Reset the ball speed
    create_bricks()  # Reset bricks
    score = 0 # reset score

# Function to render text
def render_text(text, x, y, color=(255, 255, 255)):
    text_surface = font.render(
        text, True, color
    )  # the second parameter is anti aliasing
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


create_bricks()  # Call our function to create bricks
clock = pygame.time.Clock()
game_over = False

while not game_over:
    dt = clock.tick(100)
    screen.fill((0, 0, 0))
    pressed = pygame.key.get_pressed()

    # Draw bat
    screen.blit(bat, bat_rect)
    # Draw ball
    screen.blit(ball, ball_rect)
    # Draw bricks
    for b in bricks:
        screen.blit(brick, b)

    # **** Bat movement ****
    if ball_served:
        if pressed[K_LEFT]:
            bat_rect.x -= 0.7 * dt
        if pressed[K_RIGHT]:
            bat_rect.x += 0.7 * dt

    # Restricting bat to not move out of the screen
    if bat_rect.x > screen.get_width() - bat_rect.width:
        bat_rect.x = screen.get_width() - bat_rect.width
    if bat_rect.x < 0:
        bat_rect.x = 0

    # **** Ball movement ****
    # Serve the ball with spacebar
    if pressed[K_SPACE]:
        ball_served = True

    # Check if ball is served and start movement
    if ball_served:
        ball_rect.x += sx
        ball_rect.y += sy

    # Ball collision on top of screen
    if ball_rect.y <= 0:
        sy *= -1

    # Ball collision on bottom of screen
    if ball_rect.y >= screen.get_height() - ball_rect.height:
        restart_game()

    # Ball collision on right of screen
    if ball_rect.x > screen.get_width() - ball_rect.width:
        sx *= -1

    # Ball collision on left of screen
    if ball_rect.x <= 0:
        sx *= -1

    # Check if bat makes contact with the ball
    if (
        bat_rect.x + bat_rect.width >= ball_rect.x >= bat_rect.x
        and ball_rect.y + ball_rect.height >= bat_rect.y
        and sy > 0
    ):
        relative_hit_position = (ball_rect.centerx - bat_rect.centerx) / (
            bat_rect.width / 2
        )
        # Increase difficulty everytime we hit the ball with the bat
        sy *= ball_speed_increase
        sx *= ball_speed_increase

        # Adjust horizontal direction based on where the ball hits the bat
        if relative_hit_position < 0:
            # Hit the left side of the bat
            sx = -abs(sx)
        else:
            # Hit the right side of the bat
            sx = abs(sx)
        # Reverse the vertical direction
        sy *= -1
        continue

    # Start brick to be deleted as None
    delete_brick = None

    for b in bricks:
        bx, by = b
        if (
            bx <= ball_rect.x <= bx + brick_rect.width
            and by <= ball_rect.y <= by + brick_rect.height
        ):
            delete_brick = b
            if ball_rect.x <= bx + 2:
                sx *= -1
            elif ball_rect.x >= bx + brick_rect.width - 2:
                sx *= -1
            if ball_rect.y <= by + 2:
                sy *= -1
            elif ball_rect.y >= by + brick_rect.height - 2:
                sy *= -1
            break
    # Check if any bricks have been hit and remove them
    if delete_brick is not None:
        bricks.remove(delete_brick)
        score += 1 # Update score
    
    render_text(f"Score: {score}", screen_width // 2, screen.get_height() - 50)

    # Close the window on quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    pygame.display.update()

pygame.quit()
