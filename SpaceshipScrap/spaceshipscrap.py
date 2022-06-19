"""
SpaceshipScrap is a multiplayer space shooter game designed
to showcase how everything works in pygame. Pygame is a 2D
graphics library that lets you make 2D games. In Pygame, 
everything that we are working with is usually referred to
as a surface.

__PYGAME COORDINATE SYSTEM__

- (0, 0) is in top left hand corner in Pygame.
- As you increase x coordinate you move further to right and as you decrease you move further to left
- As you increase y coordinate you move further down and as you decrease you move further up
- If you draw an image in pygame, you draw it from its top left.
"""
import pygame
import os

# Defining game setting constants
WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SpaceshipScrap') # Change heading in game window
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT) # Must subtract half the width of the border from the x coordinate to get border to appear centred.
FRAMES_PER_SECOND = 60
BULLET_VELOCITY = 7
MAX_BULLETS = 3
SPACESHIP_VELOCITY = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90) # Resize and rotate image
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_red.png'))
RED_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270) # Resize and rotate image

# Defining events constants
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Functions
def drawWindow(red, yellow, red_bullets, yellow_bullets):
    WINDOW.fill(WHITE)
    pygame.draw.rect(WINDOW, BLACK, BORDER)
    WINDOW.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y)) # blit to draw surfaces on the screen starting from top left for text and images.
    WINDOW.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))

    # Draw bullets on screen
    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    pygame.display.update() # Have to manually update display for color to show
    
def yellowMovement(keys_pressed, yellow):
    """Keyboard mappings for yellow rectangle which is moving yellow spaceship"""
    if keys_pressed[pygame.K_a] and yellow.x - SPACESHIP_VELOCITY > 0: # LEFT
        yellow.x -= SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + SPACESHIP_VELOCITY + yellow.width < BORDER.x: # RIGHT
        yellow.x += SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - SPACESHIP_VELOCITY > 0: # UP
        yellow.y -= SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + SPACESHIP_VELOCITY + yellow.width < HEIGHT: # DOWN
        yellow.y += SPACESHIP_VELOCITY

def redMovement(keys_pressed, red):
    """Keyboard mappings for red rectangle which is moving red spaceship"""
    if keys_pressed[pygame.K_LEFT] and red.x - SPACESHIP_VELOCITY > BORDER.x + BORDER.width: 
        red.x -= SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + SPACESHIP_VELOCITY + red.width < WIDTH: 
        red.x += SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - SPACESHIP_VELOCITY > 0: 
        red.y -= SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + SPACESHIP_VELOCITY + red.width < HEIGHT: 
        red.y += SPACESHIP_VELOCITY

def bulletsMovement(yellow_bullets, red_bullets, yellow, red):
    """Moves bullets, handles collision of bullets with character and handle removing of bullets when they go off screen"""
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
# Game Loop
def main():
    """Main function to run SpaceshipScrap"""
    # Define two rectangles to represent our spaceships so
    # we can control where they are moving
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets, yellow_bullets = [], []
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FRAMES_PER_SECOND) # Controls speed of while loop to ensure consistency across different machines
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)# Want bullet to move to the right
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)# Want bullet to move to the right
                    red_bullets.append(bullet)
        # Keyboard bindings
        keys_pressed = pygame.key.get_pressed()
        yellowMovement(keys_pressed, yellow)        
        redMovement(keys_pressed, red)
        bulletsMovement(yellow_bullets, red_bullets, yellow, red) # Checking if bullets collide with characters
        drawWindow(red, yellow, red_bullets, yellow_bullets)

    pygame.quit()

if __name__ == '__main__':
    main()