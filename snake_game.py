import pygame
import requests
from PIL import Image
from io import BytesIO
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

# Function to load image from URL
def load_image_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.save("background_temp.jpg")  # Save temporarily
            return pygame.image.load("background_temp.jpg")
        else:
            raise Exception(f"Failed to load image. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error loading background image: {e}")
        return None

# Load background image
background_url = "https://example.com/your-background-image.jpg"  # Replace with your URL
background_img = load_image_from_url(background_url)

# Snake settings
snake_pos = [100, 50]  # Initial position [x, y]
snake_body = [[100, 50], [90, 50], [80, 50]]  # Initial body segments
snake_direction = "RIGHT"  # Initial direction
change_to = snake_direction
speed = 15

# Food settings
food_pos = [random.randrange(1, (SCREEN_WIDTH // 10)) * 10,
            random.randrange(1, (SCREEN_HEIGHT // 10)) * 10]
food_spawn = True

# Score
score = 0

# Game over function
def game_over():
    screen.fill(WHITE)
    game_over_text = font.render(f"Game Over! Your Score: {score}", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
    quit()

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not snake_direction == "DOWN":
                change_to = "UP"
            if event.key == pygame.K_DOWN and not snake_direction == "UP":
                change_to = "DOWN"
            if event.key == pygame.K_LEFT and not snake_direction == "RIGHT":
                change_to = "LEFT"
            if event.key == pygame.K_RIGHT and not snake_direction == "LEFT":
                change_to = "RIGHT"
        if event.type == pygame.QUIT:
            running = False

    # Change direction
    if change_to == "UP":
        snake_direction = "UP"
    if change_to == "DOWN":
        snake_direction = "DOWN"
    if change_to == "LEFT":
        snake_direction = "LEFT"
    if change_to == "RIGHT":
        snake_direction = "RIGHT"

    # Move the snake
    if snake_direction == "UP":
        snake_pos[1] -= 10
    if snake_direction == "DOWN":
        snake_pos[1] += 10
    if snake_direction == "LEFT":
        snake_pos[0] -= 10
    if snake_direction == "RIGHT":
        snake_pos[0] += 10

    # Snake body growing
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawn new food
    if not food_spawn:
        food_pos = [random.randrange(1, (SCREEN_WIDTH // 10)) * 10,
                    random.randrange(1, (SCREEN_HEIGHT // 10)) * 10]
    food_spawn = True

    # Game over conditions
    if (
        snake_pos[0] < 0 or snake_pos[0] >= SCREEN_WIDTH or
        snake_pos[1] < 0 or snake_pos[1] >= SCREEN_HEIGHT
    ):
        game_over()
    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()

    # Draw elements
    screen.fill(BLACK)
    if background_img:
        screen.blit(background_img, (0, 0))  # Draw background
    for block in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], 10, 10))
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Refresh game screen
    pygame.display.update()

    # Control game speed
    clock.tick(speed)

# Quit the game
pygame.quit()
