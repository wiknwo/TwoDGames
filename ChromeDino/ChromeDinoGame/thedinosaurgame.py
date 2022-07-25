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
import pygame
import os
import random
import sys
pygame.init()
pygame.font.init()

# Defining window constants
HEIGHT = 600
WIDTH = 1100
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ChromeDino by @wiknwo')

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
        window.blit(self.image, (self.box.x, self.box.y))

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

# Game Loop
def main():
    global game_speed, x_coord_bg, y_coord_bg, obstacles, dinosaurs, points
    points = 0
    x_coord_bg = 0
    y_coord_bg = 380
    game_speed = 20

    # Nested functions
    def display_score():
        """Function to increase game difficulty, calculate and display score"""
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = GAME_FONT.render("Points: {}".format(points), True, BLACK)
        WINDOW.blit(text, (950, 50))

    def move_background():
        """Function to make background seem like it's moving"""
        global x_coord_bg, y_coord_bg
        image_width = BACKGROUND_IMAGE.get_width()
        WINDOW.blit(BACKGROUND_IMAGE, (x_coord_bg, y_coord_bg))
        WINDOW.blit(BACKGROUND_IMAGE, (image_width + x_coord_bg, y_coord_bg))
        if x_coord_bg <= -image_width:
            x_coord_bg = 0
        x_coord_bg -= game_speed

    clock = pygame.time.Clock()
    obstacles = []
    dinosaurs = [Dinosaur()]
    run = True
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
                    remove(i)
        # Taking user input
        user_input = pygame.key.get_pressed()
        for i, dinosaur in enumerate(dinosaurs):
            if user_input[pygame.K_SPACE]:
                dinosaur.isjumping = True
                dinosaur.isrunning = False
        display_score()
        move_background()
        clock.tick(30)
        pygame.display.update()

if __name__ == '__main__':
    main()