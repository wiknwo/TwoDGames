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

pygame.font.init() # Initializes pygame font library
pygame.mixer.init() # Initializes pygame sound library

# Defining window setting constants
WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SpaceshipScrap') # Change heading in game window

# Defining color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Defining game setting constants
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT) # Must subtract half the width of the border from the x coordinate to get border to appear centred.
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Gun+Silencer.mp3'))
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
FRAMES_PER_SECOND = 60
BULLET_VELOCITY = 7
MAX_BULLETS = 3
SPACESHIP_VELOCITY = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90) # Resize and rotate image
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_red.png'))
RED_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270) # Resize and rotate image
SPACE_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space.png')), (WIDTH, HEIGHT))

# Defining events constants
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Functions
def drawWindow(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    """Function to draw main game window"""
    WINDOW.blit(SPACE_BACKGROUND, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render('Health: ' + str(red_health), 1, WHITE) # Use font to render text and 1 for color aliasing
    yellow_health_text = HEALTH_FONT.render('Health: ' + str(yellow_health), 1, WHITE) # Use font to render text and 1 for color aliasing
    WINDOW.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WINDOW.blit(yellow_health_text, (10, 10))
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
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def drawWinner(text):
    """Function to display winner message"""
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000) # Pause the game for 5 seconds while we display winner

# Game Loop
def main():
    """Main function to run SpaceshipScrap"""
    # Define two rectangles to represent our spaceships so
    # we can control where they are moving
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets, yellow_bullets = [], []
    red_health, yellow_health = 10, 10
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FRAMES_PER_SECOND) # Controls speed of while loop to ensure consistency across different machines
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)# Want bullet to move to the right
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)# Want bullet to move to the right
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        winner_text = ""
        if red_health <= 0:
            winner_text = 'Yellow Wins!'
        if yellow_health <= 0:
            winner_text = 'Red Wins!'
        if winner_text != "":
            drawWinner(winner_text) # Someone won
            break
        # Keyboard bindings
        keys_pressed = pygame.key.get_pressed()
        yellowMovement(keys_pressed, yellow)        
        redMovement(keys_pressed, red)
        bulletsMovement(yellow_bullets, red_bullets, yellow, red) # Checking if bullets collide with characters
        drawWindow(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()

if __name__ == '__main__':
    main()