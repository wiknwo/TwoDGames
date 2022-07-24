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
# https://stackoverflow.com/questions/59592801/python-visual-studio-code-module-not-found
import pygame
import neat
import pickle
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

# Defining generation
GEN = 0

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
    
def draw_window(window, birds, pipes, base, score, gen):
    """Function to draw game window"""
    window.blit(BACKGROUND_IMAGE, (0, 0))
    for pipe in pipes:
        pipe.draw(window)
    text = STAT_FONT.render("Score " + str(score), 1, WHITE)
    window.blit(text, (WIDTH - 10 - text.get_width(), 50)) # Changed from 10 to 50 so I could see the score
    text = STAT_FONT.render("Gen " + str(gen), 1, WHITE)
    window.blit(text, (10, 50))
    base.draw(window)
    for bird in birds:
        bird.draw(window)
    pygame.display.update()

def main(genomes, config):
    """Function to run main game loop"""
    global GEN
    GEN += 1
    nets = []
    ge = []
    birds = []
    for genome_id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)
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
                pygame.quit()
                quit()
        # Moving objects across the screen
        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_index = 1
        else:
            run = False
            break
        for i, bird in enumerate(birds):
            bird.move()
            ge[i].fitness += 0.1
            output = nets[i].activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))
            if output[0] > 0.5:
                bird.jump()
        # Checking pipe collisions
        pipes_to_remove = []
        add_pipe = False
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[i].fitness -= 1
                    birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                pipes_to_remove.append(pipe)
            pipe.move()
        # Adding a pipe to pipes list for bird to pass
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))
        # Removing pipes that have been passed
        for pipe in pipes_to_remove:
            pipes.remove(pipe)
        # Checking if bird has hit the base
        for i, bird in enumerate(birds):
            if bird.y + bird.image.get_height() >= 730 or bird.y < 0:
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)
        base.move()
        draw_window(window, birds, pipes, base, score, GEN)

def run(config_path):
    """Function to load neat configuration details"""
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main, 50)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)