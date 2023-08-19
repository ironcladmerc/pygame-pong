import pygame
from pygame.locals import *
import random
import sys
import math

def rotate_vector(x, y, angle):
    radians = math.radians(angle)
    new_x = x * math.cos(radians) - y * math.sin(radians)
    new_y = x * math.sin(radians) + y * math.cos(radians)
    return new_x, new_y

# Initialize Pygame
pygame.init()

# Create a font object
font = pygame.font.Font(None, 72)  # You can adjust the font size as needed

# Set up the display (window) dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the window title
pygame.display.set_caption("Pong Game")

# Paddle dimensions and properties
max_spin_angle = 10
paddle_width = 15
paddle_height = 75
paddle_speed = 5

# Before the game loop
winning_score = 5

# Paddle positions
player_paddle = pygame.Rect(50, (screen_height - paddle_height) // 2, paddle_width, paddle_height)
ai_paddle = pygame.Rect(screen_width - paddle_width - 50, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)

# AI paddle properties
ai_paddle_speed = 100  # Adjust the speed as needed

# Ball properties
ball_width = 10
ball = pygame.Rect(screen_width / 2 - ball_width / 2, screen_height / 2 - ball_width / 2, ball_width, ball_width)

# Ball movement
ball_speed_x = 200
ball_speed_y = 0

# Initialize the clock
clock = pygame.time.Clock()

# Initialize delta time
delta_time = 0.0

ball.x = screen_width // 2 - ball_width // 2
ball.y = screen_height // 2 - ball_width // 2

pygame.mixer.init()  # Initialize the mixer
paddle_hit_sound = pygame.mixer.Sound('paddle_hit.wav') 
score_sound = pygame.mixer.Sound('score-1.mp3')

# Game loop
running = True
player_score = 0
ai_score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # Game loop (continued)
    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.y -= paddle_speed
    if keys[pygame.K_s] and player_paddle.bottom < screen_height:
        player_paddle.y += paddle_speed

    # AI paddle movement (follow the ball's y position)
    if ai_paddle.centery < ball.centery:
        ai_paddle.y += ai_paddle_speed * delta_time
    if ai_paddle.centery > ball.centery:
        ai_paddle.y -= ai_paddle_speed * delta_time

    if ai_paddle.top > 0:
        ai_paddle.y -= paddle_speed
    if ai_paddle.bottom < screen_height:
        ai_paddle.y += paddle_speed
   
    # Calculate delta time
    delta_time = clock.tick(60) / 1000.0  # 60 frames per second
    
    # Move the ball
    ball.x += ball_speed_x * delta_time
    ball.y += ball_speed_y * delta_time

    # Ball collision with walls
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y = -ball_speed_y

    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(ai_paddle):
        ball_speed_x = -ball_speed_x
        paddle_hit_sound.play()  # Play the sound effect

        # Adjust ball's vertical speed based on collision point
        collision_point = (ball.centery - (player_paddle.centery + ai_paddle.centery) / 2) / (player_paddle.height / 2)

        ball_speed_y = collision_point * 100 # Adjust the factor as needed

        # Apply spin angle based on collision point
        spin_angle = collision_point * max_spin_angle  # Adjust max_spin_angle as needed
        ball_speed_x, ball_speed_y = rotate_vector(ball_speed_x, ball_speed_y, spin_angle)

    # Check if ball crosses boundaries
    if ball.right >= screen_width:
        # Player scores a point
        player_score += 1
        score_sound.play()
        if player_score < 5:
           ball.x = screen_width // 2 - ball_width // 2
           ball.y = screen_height // 2 - ball_width // 2
           ball_speed_y = 0
           ball_speed_x = 200
    elif ball.left <= 0:
        # AI scores a point
        ai_score += 1
        score_sound.play()
        if ai_score < 5:
            ball.x = screen_width // 2 - ball_width // 2
            ball.y = screen_height // 2 - ball_width // 2
            ball_speed_y = 0
            ball_speed_x = 200

    # Check for a winner
    if player_score >= winning_score or ai_score >= winning_score:
        running = False  # End the game loop

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw paddles
    pygame.draw.rect(screen, (255, 255, 255), player_paddle)
    pygame.draw.rect(screen, (255, 255, 255), ai_paddle)

    # Draw the ball
    pygame.draw.rect(screen, (255, 255, 255), ball)

    # Draw the centerline
    # pygame.draw.line(screen, (255, 255, 255), (screen_width // 2, 0), (screen_width // 2, screen_height), 10)

    # Draw the dotted centerline
    dot_interval = 10  # Adjust the interval between dots
    for y in range(0, screen_height, dot_interval * 2):
        pygame.draw.line(screen, (255, 255, 255), (screen_width // 2, y), (screen_width // 2, y + dot_interval), 1)

    # Display the scores
    player_score_text = font.render(str(player_score), True, (255, 255, 255))
    ai_score_text = font.render(str(ai_score), True, (255, 255, 255))
    screen.blit(player_score_text, (20, 20))  # Adjust the position as needed
    screen.blit(ai_score_text, (screen_width - ai_score_text.get_width() - 20, 20))

    # Update the display
    pygame.display.flip()

    # Quit the game if the window is closed

# Game over state
if player_score >= winning_score:
    game_over_text = font.render("Player 1 Wins", True, (255, 255, 255))
elif ai_score >= winning_score:
    game_over_text = font.render("Player 2 Wins", True, (255, 255, 255))
else: 
    game_over_text = font.render("Game Over", True, (255, 255, 255))

screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
pygame.display.flip()

pygame.mixer.quit()

# Wait for a moment before quitting
pygame.time.wait(3000)  # Wait for 2 seconds

# Quit Pygame
pygame.quit()
