"""
The Dinosaur Game (also known as the Chrome Dino) is a 
browser game developed by Google and built into the Google 
Chrome web browser. The player guides a pixelated 
Tyrannosaurus rex across a side-scrolling landscape, 
avoiding obstacles to achieve a higher score. The game was 
created by members of the Chrome UX team in 2014.
During the game, the Lonely T-Rex continuously moves from 
left to right across a black-and-white desert landscape, 
with the player attempting to avoid oncoming obstacles 
such as cacti and Pteranodons by jumping or ducking. As the 
game progresses, the speed of play gradually increases 
until the user hits an obstacle, prompting an instant game 
over.
"""
# https://stackoverflow.com/questions/61365668/applying-saved-neat-python-genome-to-test-environment-after-training
# https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
import pygame
import os
import random
import sys
import neat
import math
import pickle
pygame.init()
pygame.font.init()

# Defining window constants
HEIGHT = 600
WIDTH = 1100
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ChromeDinoAI by @wiknwo')

# Loading images
DINO_RUNNING_IMAGES = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")), pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
DINO_JUMPING_IMAGE =  pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
BACKGROUND_IMAGE = pygame.image.load(os.path.join("Assets/Other", "Track.png"))
SMALL_CACTUS_IMAGES = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")), pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")), pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS_IMAGES = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")), pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")), pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

# Setting up fonts
GAME_FONT = pygame.font.SysFont('Roboto', 20)

# Defining colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Defining number of generations
GENERATIONS = 0

class Dinosaur:
    # Static variables
    X_COORD = 80
    Y_COORD = 310
    JUMP_VELOCITY = 8.5

    def __init__(self, image=DINO_RUNNING_IMAGES[0]):
        """Initializes variables for dinosaur"""
        self.image = image
        self.isrunning = True
        self.isjumping = False
        self.jump_velocity = self.JUMP_VELOCITY
        self.box = pygame.Rect(self.X_COORD, self.Y_COORD, image.get_width(), image.get_height()) # Places a box around our dinosaur
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.step_index = 0 # Cycles through images of running dinosaur

    def update(self):
        """Method to check which state the dinosaur is in and call the appropriate function"""
        if self.isrunning:
            self.run()
        if self.isjumping:
            self.jump()
        if self.step_index >= 10:
            self.step_index = 0

    def jump(self):
        """Method to make dinosaur jump"""
        self.image = DINO_JUMPING_IMAGE
        if self.isjumping:
            self.box.y -= self.jump_velocity * 4
            self.jump_velocity -= 0.8
        if self.jump_velocity <= -self.JUMP_VELOCITY:
            self.isjumping = False
            self.isrunning = True
            self.jump_velocity = self.JUMP_VELOCITY

    def run(self):
        """Method to make dinosaur run"""
        self.image = DINO_RUNNING_IMAGES[self.step_index // 5]
        self.box.x = self.X_COORD
        self.box.y = self.Y_COORD
        self.step_index += 1

    def draw(self, window):
        """Method to draw dinosaur on window"""
        # Draw dinosaur on window
        window.blit(self.image, (self.box.x, self.box.y))
        # Draw hitbox surrounding dinosaur
        pygame.draw.rect(window, self.color, (self.box.x, self.box.y, self.box.width, self.box.height), 2)
        # Draw dinosaur's line of sight from eye to nearest obstacle
        for obstacle in obstacles:
            pygame.draw.line(window, self.color, (self.box.x + 54, self.box.y + 12), obstacle.box.center, 2)

class Obstacle:
    def __init__(self, image, cacti_count):
        """Initializes object with necessary variables"""
        self.image = image
        self.type = cacti_count
        self.box = self.image[self.type].get_rect()
        self.box.x = WIDTH

    def update(self):
        """Method to update obstacle"""
        self.box.x -= game_speed
        if self.box.x < -self.box.width:
            obstacles.pop()

    def draw(self, window):
        """Method to draw obstacle"""
        window.blit(self.image[self.type], self.box)

class SmallCactus(Obstacle):
    def __init__(self, image, cacti_count):
        """Initializes small cactus"""
        super().__init__(image, cacti_count)
        self.box.y = 325
        
class LargeCactus(Obstacle):
    def __init__(self, image, cacti_count):
        super().__init__(image, cacti_count)
        self.box.y = 300

def remove(index):
    """Function to remove dinosaur that runs into obstacle"""
    dinosaurs.pop(index)
    ge.pop(index)
    nets.pop(index)

def distance(a_coords, b_coords):
    """Function to calculate euclidean distance between two sets of coordinates"""
    dx = a_coords[0] - b_coords[0]
    dy = a_coords[1] - b_coords[1]
    return math.sqrt(dx**2 + dy**2)

# Game Loop
def eval_genomes(genomes, config):
    global game_speed, x_coord_bg, y_coord_bg, obstacles, dinosaurs, ge, nets, points, GENERATIONS
    GENERATIONS += 1
    points = 0
    x_coord_bg = 0
    y_coord_bg = 380
    game_speed = 20
    clock = pygame.time.Clock()
    obstacles = []
    dinosaurs = []
    ge = [] # List of dictionaries containing information on each dinosaur
    nets = []
    run = True

    for genome_id, genome in genomes:
        dinosaurs.append(Dinosaur())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    # Nested functions
    def display_score():
        """Function to increase game difficulty, calculate and display score"""
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = GAME_FONT.render("Points: {}".format(points), True, BLACK)
        WINDOW.blit(text, (950, 50))

    def display_stats():
        """Function to display stats of the game and AI"""
        global dinosaurs, game_speed, ge
        text_1 = GAME_FONT.render('Dinosaurs Alive: {}'.format(str(len(dinosaurs))), True, BLACK)
        text_2 = GAME_FONT.render('Generation: {}'.format(str(GENERATIONS)), True, BLACK)
        text_3 = GAME_FONT.render('Game Speed: {}'.format(str(game_speed)), True, BLACK)
        WINDOW.blit(text_1, (50, 450))
        WINDOW.blit(text_2, (50, 480))
        WINDOW.blit(text_3, (50, 510))

    def move_background():
        """Function to make background seem like it's moving"""
        global x_coord_bg, y_coord_bg
        image_width = BACKGROUND_IMAGE.get_width()
        WINDOW.blit(BACKGROUND_IMAGE, (x_coord_bg, y_coord_bg))
        WINDOW.blit(BACKGROUND_IMAGE, (image_width + x_coord_bg, y_coord_bg))
        if x_coord_bg <= -image_width:
            x_coord_bg = 0
        x_coord_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        # Refreshing the window on each iteration
        WINDOW.fill(WHITE)
        # Drawing the dinosaurs on the window
        for dinosaur in dinosaurs:
            dinosaur.update()
            dinosaur.draw(WINDOW)

        # Checking if there are any dinosaurs left
        if len(dinosaurs) == 0:
            break
        # Randomly generating obstacles
        if len(obstacles) == 0:
            rand_int = random.randint(0, 1)
            if rand_int == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS_IMAGES, random.randint(0, 2)))
            elif rand_int == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS_IMAGES, random.randint(0, 2)))
        # Drawing obstacles
        for obstacle in obstacles:
            obstacle.draw(WINDOW)
            obstacle.update()
            # Checking if dinosaurs collide with obstacles
            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.box.colliderect(obstacle.box):
                    ge[i].fitness -= 1
                    remove(i)
                else:
                    ge[i].fitness += 5
        # Taking user input
        for i, dinosaur in enumerate(dinosaurs):
            output = nets[i].activate((dinosaur.box.y, distance((dinosaur.box.x, dinosaur.box.y), obstacle.box.midtop)))
            if output[0] > 0.5 and dinosaur.box.y == dinosaur.Y_COORD:
                dinosaur.isjumping = True
                dinosaur.isrunning = False
        display_stats()
        display_score()
        move_background()
        clock.tick(30)
        pygame.display.update()

def replay_genome(config_path, genome_path="winner.pickle"):
    # Load required NEAT config
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    # Unpickle saved winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)
        f.close()
    # Convert loaded genome into required data structure
    genomes = [(1, genome)]
    # Call game with only the loaded genome
    eval_genomes(genomes, config)

def run(config_path):
    """Function to load neat configuration details"""
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(eval_genomes, 50) # Passing fitness function and max number of generations to run
    # Save best genome
    with open("winner.pickle", "wb") as f:
        pickle.dump(winner, f)
        f.close()

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    # Check if 'winner.pickle' file already exists
    if os.path.isfile("winner.pickle"):
        replay_genome(config_path)
    else:
        run(config_path)