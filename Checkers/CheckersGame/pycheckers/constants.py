import pygame

# Display settings
WIDTH, HEIGHT = 600, 600
ROWS, COLUMNS = 8, 8
SQUARE_SIZE = WIDTH // COLUMNS

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

# Loading images
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (45, 25)) # assets needs to be in top-level directory for python to find file