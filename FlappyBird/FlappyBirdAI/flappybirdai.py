"""
Flappy Bird is a mobile game developed by Vietnamese video 
game artist and programmer Dong Nguyen under his game 
development company '.Gears'. The game is a side-scroller 
where the player controls a bird, attempting to fly between 
columns of green pipes without hitting them. Flappy Bird is 
an arcade-style game in which the player controls the bird 
Faby, which moves persistently to the right. The player is 
tasked with navigating Faby through pairs of pipes that 
have equally sized gaps placed at random heights. Faby 
automatically descends and only ascends when the player 
taps the touchscreen. Each successful pass through a pair 
of pipes awards the player one point. Colliding with a 
pipe or the ground ends the gameplay. During the game over 
screen, the player is awarded a bronze medal if they 
reached ten or more points, a silver medal from twenty 
points, a gold medal from thirty points, and a platinum 
medal from forty points.
"""
import pygame
import neat
import time
import os
import random
pygame.font.init()

# Defining game window constants
WIDTH = 600
HEIGHT = 800

# Loading images
BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))]
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))

# Setting fonts
STAT_FONT = pygame.font.SysFont("roboto", 50)

# Defining colors
WHITE = (255, 255, 255)

class Bird:
    # Class constants (static variables)
    MAX_ROTATION = 25 # How much the bird will tilt upwards or donwards
    ROTATION_VELOCITY = 20 # How much the bird will rotate on each frame or when we move the bird
    ANIMATION_TIME = 5 # How long we will show each bird animation

    def __init__(self, x, y):
        """Initializes variables for flappy bird"""
        self.x = x
        self.y = y
        self.tilt = 0 # How much the bird is actually tilted so we can draw it on the screen
        self.tick_count = 0 # Keeps track of when we last jumped
        self.velocity = 0
        self.height = self.y
        self.image_index = 0 # Count representing which bird image we are showing
        self.image = BIRD_IMAGES[0]

    def jump(self):
        """Method to make Faby jump"""
        self.velocity = -10.5
        self.tick_count = 0 # Reset to zero so we know when we are changing velocity
        self.height = self.y

    def move(self):
        """Method to be called every single frame to move Faby on the screen"""
        self.tick_count += 1
        # Calculating bird's displacement
        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count**2 # Tells us distance bird is moving in upward or downward direction
        if displacement >= 16: 
            displacement = 16 # Set terminal velocity for bird if it is over a certain velocity
        if displacement < 0: 
            displacement -= 2
        self.y += displacement
        # Calculating bird's tilt
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY
    
    def draw(self, window):
        """Method to draw the bird"""
        self.image_index += 1
        if self.image_index < self.ANIMATION_TIME:
            self.image = BIRD_IMAGES[0]
        elif self.image_index < self.ANIMATION_TIME * 2:
            self.image = BIRD_IMAGES[1]
        elif self.image_index < self.ANIMATION_TIME * 3:
            self.image = BIRD_IMAGES[2]
        elif self.image_index < self.ANIMATION_TIME * 4:
            self.image = BIRD_IMAGES[1]
        elif self.image_index < self.ANIMATION_TIME * 4 + 1:
            self.image = BIRD_IMAGES[0]
            self.image_index = 0
        if self.tilt <= -80:
            self.image = BIRD_IMAGES[1]
            self.image_index = self.ANIMATION_TIME * 2
        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft = (self.x, self.y)).center)
        window.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        """Method to get 2D bitmask for image"""
        return pygame.mask.from_surface(self.image)

class Pipe:
    # Class constants
    GAP = 200
    VELOCITY = 5

    def __init__(self, x):
        """Initializes pipe variables"""
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = PIPE_IMAGE
        self.passed = False # Indicates if bird has passsed this pipe
        self.set_height()

    def set_height(self):
        """Method to randomly set height for this pipe"""
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """Method to move pipe across screen"""
        self.x -= self.VELOCITY

    def draw(self, window):
        """Method to draw pipe top and bottom"""
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    
    def collide(self, bird):
        """Method to check if bird collides with pipe"""
        bird_mask = bird.get_mask()
        pipe_top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        pipe_bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        pipe_top_offset = (self.x - bird.x, self.top - round(bird.y)) # Offset from bird to top pipe
        pipe_bottom_offset = (self.x - bird.x, self.bottom - round(bird.y)) # Offset from bird to bottom pipe
        # Checking for collision: Pixel overlap
        bottom_touch = bird_mask.overlap(pipe_bottom_mask, pipe_bottom_offset)
        top_touch = bird_mask.overlap(pipe_top_mask, pipe_top_offset)
        return top_touch or bottom_touch

class Base:
    # Class constants
    VELOCITY = 5 # Must move at same speed as pipe
    WIDTH = BASE_IMAGE.get_width()

    def __init__(self, y):
        """Initializes Base variables"""
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """Method to move base image across screen"""
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY
        # As soon as first image moves off screen then
        # cycle the second image to move onto the screen
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, window):
        """Method to draw base onto screen"""
        window.blit(BASE_IMAGE, (self.x1, self.y))
        window.blit(BASE_IMAGE, (self.x2, self.y))
    
def draw_window(window, bird, pipes, base, score):
    """Function to draw game window"""
    window.blit(BACKGROUND_IMAGE, (0, 0))
    for pipe in pipes:
        pipe.draw(window)
    text = STAT_FONT.render("Score " + str(score), 1, WHITE)
    window.blit(text, (WIDTH - 10 - text.get_width(), 50)) # Changed from 10 to 50 so I could see the score
    base.draw(window)
    bird.draw(window)
    pygame.display.update()

def main():
    """Function to run main game loop"""
    faby = Bird(230, 350)
    base = Base(700)
    pipes = [Pipe(600)]
    score = 0
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # Moving objects across the screen
        #faby.move()
        pipes_to_remove = []
        add_pipe = False
        for pipe in pipes:
            if pipe.collide(faby):
                pass
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                pipes_to_remove.append(pipe)
            if not pipe.passed and pipe.x < faby.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()
        # Adding a pipe to pipes list for bird to pass
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
        # Removing pipes that have been passed
        for pipe in pipes_to_remove:
            pipes.remove(pipe)
        # Checking if bird has hit the base
        if faby.y + faby.image.get_height() >= 730:
            pass
        base.move()
        draw_window(window, faby, pipes, base, score)
    pygame.quit()
    quit()

if __name__ == '__main__':
    main()