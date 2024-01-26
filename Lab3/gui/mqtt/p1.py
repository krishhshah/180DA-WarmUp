import paho.mqtt.client as mqtt
import numpy as np
import time
import pygame
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

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 500

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


p1_win = 0
p2_win = 0
tie = 0

result_ready = False
result = 4
start = 0
p2_move = 3
first_run = True


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
tab_text = font.render(f'Player 1: {p1_win} | Player 2: {p2_win} | Tie: {tie}', True, (0,0,0), (255,255,255))          

# create a rectangular object for the
# text surface object
choose_results_textRect = choose_results_text.get_rect()
tab_textRect = tab_text.get_rect()


# set the center of the rectangular object.
choose_results_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5)
tab_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)


# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ece180d/krish/p1_in", qos=1)

# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

# The default message callback.
# (you can create separate callbacks per subscribed topic)
def on_message(client, userdata, message):
    message.payload = message.payload.decode("utf-8")
    global p1_win
    global p2_win
    global tie
    global result
    global result_ready
    global p2_move
    # print('Received message: "'+ str(message.payload) + '" on topic "' +
    #     message.topic + '" with QoS ' + str(message.qos))
    if str(message.payload) == 'start':
        pass
    elif str(message.payload) == '0':
        print('Waiting on Player 2.')
        result_ready = False
        result = 0
    else:
        p2_int = str(message.payload)[2]
        if p2_int == '0':
            p2_move = 'rock'
        elif p2_int == '1':
            p2_move = 'paper'
        elif p2_int == '2':
            p2_move = 'scissors'

        result = int(str(message.payload)[0])
        result_ready = True

    
# 1. create a client instance.
client = mqtt.Client()
# add additional client options (security, certifications, etc.)
# many default options should be good to start off.
# add callbacks to client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# 2. connect to a broker using one of the connect*() functions.
# client.connect_async("test.mosquitto.org")
client.connect_async('mqtt.eclipseprojects.io')
# client.connect("test.mosquitto.org", 1883, 60)
# client.connect("mqtt.eclipse.org")

# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()
# client.loop_forever()

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards

# Define constants for the screen width and height


# Variable to keep the main loop running
running = True
query = True
choices = ['rock', 'paper', 'scissors']

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONUP and query:
            mouse_loc = pygame.mouse.get_pos()
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
                client.publish("ece180d/krish/p1_out", player, qos=1)

    if not result_ready and result == 0:
        choose_results_text = font.render('Waiting for Player 2...', True, (0,0,0), (255,255,255))
    elif result_ready:
        if result == 1:
            p1_win += 1
            choose_results_text = font.render(f'You win! Player 2 chose {p2_move}', True, (0,0,0), (255,255,255))
        elif result == 2:
            p2_win += 1
            choose_results_text = font.render(f'You lose! Player 2 chose {p2_move}', True, (0,0,0), (255,255,255))
        elif result == 3:
            tie += 1
            choose_results_text = font.render(f'It was a tie! You both chose {p2_move}', True, (0,0,0), (255,255,255))
        first_run = False
        start = time.time()
        result_ready = False
        result = 4
        

    if time.time()-start>=3 and not first_run:
        first_run = True
        query = True
        choose_results_text = font.render('Choose Rock, Paper, or Scissors', True, (0,0,0), (255,255,255))

    tab_text = font.render(f'Player 1: {p1_win} | Player 2: {p2_win} | Tie: {tie}', True, (0,0,0), (255,255,255))          


    choose_results_textRect = choose_results_text.get_rect()
    tab_textRect = tab_text.get_rect()


    # set the center of the rectangular object.
    choose_results_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5)
    tab_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        
    # Fill the screen with black
    screen.fill((255, 255, 255))

    # Draw the player on the screen
    screen.blit(rock.surf, (SCREEN_WIDTH / 7, SCREEN_HEIGHT / 2))
    screen.blit(paper.surf, (SCREEN_WIDTH*3 / 7, SCREEN_HEIGHT / 2))
    screen.blit(scissors.surf, (SCREEN_WIDTH*5 / 7, SCREEN_HEIGHT / 2))
    screen.blit(choose_results_text, choose_results_textRect)
    screen.blit(tab_text, tab_textRect)

    # Update the display
    pygame.display.flip()# do your non-blocked other stuff here, like receive IMU data or something.
# use subscribe() to subscribe to a topic and receive messages.

# use publish() to publish messages to the broker.

# use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()