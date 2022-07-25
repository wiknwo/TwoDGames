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

# Setting up fonts
GAME_FONT = pygame.font.SysFont('Roboto', 20)

# Defining colors
WHITE = (255, 255, 255)

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

# Game Loop
def main():
    clock = pygame.time.Clock()
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
        # Taking user input
        user_input = pygame.key.get_pressed()
        for i, dinosaur in enumerate(dinosaurs):
            if user_input[pygame.K_SPACE]:
                dinosaur.isjumping = True
                dinosaur.isrunning = False
        clock.tick(30)
        pygame.display.update()

if __name__ == '__main__':
    main()