"""
SpaceshipScrap is a multiplayer space shooter game designed
to showcase how everything works in pygame. Pygame is a 2D
graphics library that lets you make 2D games. In Pygame, 
everything that we are working with is usually referred to
as a surface.
"""
import pygame

# Defining constants
WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# Game Loop
def main():
    """Main function to run SpaceshipScrap"""
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

if __name__ == '__main__':
    main()