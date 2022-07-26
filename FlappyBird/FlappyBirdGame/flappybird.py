import pygame
import sys
import random
pygame.init()
pygame.font.init()

# Define window constants
WIDTH = 551
HEIGHT = 620 # 720
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('FlappyBird by @wiknwo')

# Loading images
BIRD_IMAGES = [pygame.image.load("assets/bird_down.png"), pygame.image.load("assets/bird_mid.png"), pygame.image.load("assets/bird_up.png")]
SKYLINE_IMAGE = pygame.image.load("assets/background.png")
GROUND_IMAGE = pygame.image.load("assets/ground.png")
TOP_PIPE_IMAGE = pygame.image.load("assets/pipe_top.png")
BOTTOM_PIPE_IMAGE = pygame.image.load("assets/pipe_bottom.png")
GAME_OVER_IMAGE = pygame.image.load("assets/game_over.png")
START_IMAGE = pygame.image.load("assets/start.png")

# Defining game constants and variables
FRAMES_PER_SECOND = 60
scroll_speed = 1
bird_start_position = (100, 200) # (100, 250)
score = 0
game_stopped = True
GAME_FONT = pygame.font.SysFont('Roboto', 26)

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = BIRD_IMAGES[0]
        self.rect = self.image.get_rect()
        self.rect.center = bird_start_position
        self.image_index = 0
        self.velocity = 0
        self.flap = False
        self.alive = True

    def update(self, user_input):
        if self.alive:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = BIRD_IMAGES[self.image_index // 10]
        # Gravity and flap
        self.velocity += 0.5
        if self.velocity > 7:
            self.velocity = 7
        if self.rect.y < 400: # 500
            self.rect.y += int(self.velocity)
        if self.velocity == 0:
            self.flap = False
        # Rotate bird
        self.image = pygame.transform.rotate(self.image, self.velocity * -7)
        # User input
        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
            self.flap = True
            self.velocity = -7

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.exit, self.passed = False, False, False
        self.pipe_type = pipe_type

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -WIDTH:
            self.kill()
        # Update the score
        global score
        if self.pipe_type == 'bottom':
            if bird_start_position[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if bird_start_position[0] > self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                score += 1

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """Initializes ground with image"""
        pygame.sprite.Sprite.__init__(self)
        self.image = GROUND_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        """Moves ground from RHS of screen to LHS"""
        self.rect.x -= scroll_speed
        # When ground moves off the screen we want to delete it
        if self.rect.x <= -WIDTH:
            self.kill()

# Game loop
def main():
    global score
    # Create bird object
    faby = pygame.sprite.GroupSingle()
    faby.add(Bird())
    # Create pipes
    pipe_timer = 0
    pipes = pygame.sprite.Group()
    # Create ground object
    x_pos_ground, y_pos_ground = 0, 420 # (0, 520)
    ground = pygame.sprite.Group()
    ground.add(Ground(x_pos_ground, y_pos_ground))
    clock = pygame.time.Clock()
    run = True
    while run:
        # Logic to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Reset frame
        WINDOW.fill(BLACK)

        # User input
        user_input = pygame.key.get_pressed()

        # Draw background
        WINDOW.blit(SKYLINE_IMAGE, (0, 0))

        # Spawn ground
        if len(ground) <= 2:
            ground.add(Ground(WIDTH, y_pos_ground))

        # Draw pipes, ground and bird
        pipes.draw(WINDOW)
        ground.draw(WINDOW)
        faby.draw(WINDOW)
        
        # Display score
        score_text = GAME_FONT.render('Score: ' + str(score), True, WHITE)
        WINDOW.blit(score_text, (20, 20))

        # Update pipes, ground and bird
        if faby.sprite.alive:
            pipes.update()
            ground.update()
        faby.update(user_input)

        # Collision Detection
        collision_pipes = pygame.sprite.spritecollide(faby.sprites()[0], pipes, False)
        collision_ground = pygame.sprite.spritecollide(faby.sprites()[0], ground, False)
        if collision_pipes or collision_ground:
            faby.sprite.alive = False
            if collision_ground:
                WINDOW.blit(GAME_OVER_IMAGE, (WIDTH // 2 - GAME_OVER_IMAGE.get_width() // 2, HEIGHT // 2 - GAME_OVER_IMAGE.get_height() // 2))
                if user_input[pygame.K_SPACE]:
                    score = 0
                    break
        # Spawn pipes
        if pipe_timer <= 0 and faby.sprite.alive:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(90, 130) + BOTTOM_PIPE_IMAGE.get_height()
            pipes.add(Pipe(x_top, y_top, TOP_PIPE_IMAGE, 'top'))
            pipes.add(Pipe(x_bottom, y_bottom, BOTTOM_PIPE_IMAGE, 'bottom'))
            pipe_timer = random.randint(180, 250)
        pipe_timer -= 1

        clock.tick(FRAMES_PER_SECOND)
        pygame.display.update()

def menu():
    global game_stopped
    while game_stopped:
        # Logic to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Draw menu
        WINDOW.fill(BLACK)
        WINDOW.blit(SKYLINE_IMAGE, (0, 0))
        WINDOW.blit(GROUND_IMAGE, Ground(0, 420))
        WINDOW.blit(BIRD_IMAGES[0], (100, 200))
        WINDOW.blit(START_IMAGE, (WIDTH // 2 - START_IMAGE.get_width() // 2, HEIGHT // 2 - START_IMAGE.get_height() // 2))
        # User input
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            main()
        pygame.display.update()

if __name__ == '__main__':
    menu()
