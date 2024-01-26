# Import the pygame module
import pygame
import random as r
import time


# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
start = 0




r_pic = pygame.image.load("/Users/krish/Desktop/ECE180DA/180DA-WarmUp/Lab3/gui/pictures/rock.png")
p_pic = pygame.image.load("/Users/krish/Desktop/ECE180DA/180DA-WarmUp/Lab3/gui/pictures/paper.png")
s_pic = pygame.image.load("/Users/krish/Desktop/ECE180DA/180DA-WarmUp/Lab3/gui/pictures/scissors.png")

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        super(Rock, self).__init__()
        self.surf = r_pic.convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft=(SCREEN_WIDTH/4, SCREEN_HEIGHT/2))
class Paper(pygame.sprite.Sprite):
    def __init__(self):
        super(Paper, self).__init__()
        self.surf = p_pic.convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
class Scissors(pygame.sprite.Sprite):
    def __init__(self):
        super(Scissors, self).__init__()
        self.surf = s_pic.convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft=(SCREEN_WIDTH*3/4, SCREEN_HEIGHT/2))

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Instantiate player. Right now, this is just a rectangle.
rock = Rock()
paper = Paper()
scissors = Scissors()





font = pygame.font.Font('freesansbold.ttf', 32)

# create a text surface object,
# on which text is drawn on it.
choose_results_text = font.render('Choose Rock, Paper, or Scissors', True, (0,0,0), (255,255,255))
tab_text = font.render('Player: 0 | Computer: 0 | Tie: 0', True, (0,0,0), (255,255,255))

# create a rectangular object for the
# text surface object
choose_results_textRect = choose_results_text.get_rect()
tab_textRect = tab_text.get_rect()


# set the center of the rectangular object.
choose_results_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5)
tab_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)





# Variable to keep the main loop running
running = True
query = True
tie = 0
p_win = 0
c_win = 0
choices = ['rock', 'paper', 'scissors']

# Main loop
while running:
    # for loop through the event queue
    if query == True:
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_loc = pygame.mouse.get_pos()
                computer = r.randrange(3)
                computer_string = choices[computer]
                player = 3
                if rock.rect.collidepoint(mouse_loc):
                    player = 0
                    player_string = 'rock'
                elif paper.rect.collidepoint(mouse_loc):
                    player = 1
                    player_string = 'paper'
                elif scissors.rect.collidepoint(mouse_loc):
                    player = 2
                    player_string = 'scissors'
                if player != 3:
                    query = False
                    start = time.time()
                    if computer == player:
                        print("Tie: ")
                        tie+=1
                        choose_results_text = font.render(f'You chose {player_string}. Computer chose {computer_string}. Tie!', True, (0,0,0), (255,255,255))
                    elif (computer - player) == 2 or player > computer:
                        print("Player wins: ")
                        p_win += 1
                        choose_results_text = font.render(f'You chose {player_string}. Computer chose {computer_string}. You Win!', True, (0,0,0), (255,255,255))
                    elif (computer - player) == -2 or computer > player:
                        print("Computer wins: ")
                        c_win += 1
                        choose_results_text = font.render(f'You chose {player_string}. Computer chose {computer_string}. You Lose!', True, (0,0,0), (255,255,255))
                    tab_text = font.render(f'Player: {p_win} | Computer: {c_win} | Tie: {tie}', True, (0,0,0), (255,255,255))          

    if time.time()-start>=3:
        query = True
        choose_results_text = font.render('Choose Rock, Paper, or Scissors', True, (0,0,0), (255,255,255))


    choose_results_textRect = choose_results_text.get_rect()
    choose_results_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5)
        
    # Fill the screen with black
    screen.fill((255, 255, 255))

    # Draw the player on the screen
    screen.blit(rock.surf, (SCREEN_WIDTH / 7, SCREEN_HEIGHT / 2))
    screen.blit(paper.surf, (SCREEN_WIDTH*3 / 7, SCREEN_HEIGHT / 2))
    screen.blit(scissors.surf, (SCREEN_WIDTH*5 / 7, SCREEN_HEIGHT / 2))
    screen.blit(choose_results_text, choose_results_textRect)
    screen.blit(tab_text, tab_textRect)

    # Update the display
    pygame.display.flip()

pygame.quit()