"""
Hangman is a guessing game for two or more players. One 
player thinks of a word, phrase or sentence and the other(s) 
tries to guess it by suggesting letters within a certain 
number of guesses.
"""
import pygame
import math
import random

pygame.init()

# Defining constants: No notion of constants in Python* and setting up display
WIDTH, HEIGHT = 800, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hangman by @wiknwo')
FRAMES_PER_SECOND = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RADIUS = 20
GAP = 15
letters = [] # (x-coordinate, y-coordinate, letter, isVisibleBoolean)
START_X = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
START_Y = 400
LETTER_FONT = pygame.font.SysFont('comicsans', 30)
WORD_FONT = pygame.font.SysFont('comicsans', 30)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# Initializing letters list
for i in range(26):
    x = START_X + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = START_Y + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(65 + i), True])

# Load images
images = []
for i in range(7):
    images.append(pygame.image.load('images/hangman' + str(i) + '.png'))

# Game variables
hangman_status = 0 # Tells us which image to draw at each point in the game
words = ['RUBY', 'PYTHON', 'SCALA', 'KOTLIN', 'JAVA']
word = random.choice(words)
guesses = [] # Letters guessed by player

# Define game loop settings
clock = pygame.time.Clock()
run = True

# Functions
def draw():
    """Function to draw images onto screen"""
    window.fill(WHITE) # Fill entire screen with color
    # Draw title
    text = TITLE_FONT.render('HANGMAN', 1, BLACK)
    window.blit(text, (WIDTH / 2 - text.get_width() / 2, 10))
    # Draw word
    display_word = ''
    for letter in word:
        if letter in guesses:
            display_word += letter + ' '
        else:
            display_word += '_ '
    text = WORD_FONT.render(display_word, 1, BLACK)
    window.blit(text, (400, 200)) # Modify (x, y) depending on length of word
    # Draw buttons
    for letter in letters:
        x, y, character, isVisible = letter
        if isVisible:
            pygame.draw.circle(window, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(character, 1, BLACK) # 1 is for anti-aliasing
            window.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))
    window.blit(images[hangman_status], (150, 100)) # Draw an image or surface
    pygame.display.update() # Update display with any of the most recent things we have drawn on it

def displayMessage(message):
    pygame.time.delay(1000)
    window.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    window.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)

# Game Loop
while run:
    clock.tick(FRAMES_PER_SECOND)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, character, isVisible = letter
                if isVisible:
                    distance = math.sqrt((x - mouse_x)**2 + (y - mouse_y)**2)
                    if distance < RADIUS:
                        letter[3] = False
                        guesses.append(character)
                        if character not in word:
                            hangman_status += 1
    draw()
    hasWon = True
    for letter in word:
        if letter not in guesses:
            hasWon = False
            break
    if hasWon:
        displayMessage('YOU WON!')
        break
    if hangman_status == 6:
        displayMessage('YOU LOST!')
        break

pygame.quit()