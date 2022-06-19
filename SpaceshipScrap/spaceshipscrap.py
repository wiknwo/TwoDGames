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

# Defining constants
WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SpaceshipScrap') # Change heading in game window
WHITE = (255, 255, 255)
FRAMES_PER_SECOND = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90) # Resize and rotate image
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_red.png'))
RED_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270) # Resize and rotate image

# Functions
def drawWindow(red, yellow):
    WINDOW.fill(WHITE)
    WINDOW.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y)) # blit to draw surfaces on the screen starting from top left for text and images.
    WINDOW.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))
    pygame.display.update() # Have to manually update display for color to show

# Game Loop
def main():
    """Main function to run SpaceshipScrap"""
    # Define two rectangles to represent our spaceships so
    # we can control where they are moving
    red = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FRAMES_PER_SECOND) # Controls speed of while loop to ensure consistency across different machines
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        red.x += 1 # Will move 60 pixels per second
        drawWindow(red, yellow)
    pygame.quit()

if __name__ == '__main__':
    main()