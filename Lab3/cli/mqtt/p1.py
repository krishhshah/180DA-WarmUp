import paho.mqtt.client as mqtt
import numpy as np
import time

p1_win = 0
p2_win = 0
tie = 0

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
    # print('Received message: "'+ str(message.payload) + '" on topic "' +
    #     message.topic + '" with QoS ' + str(message.qos))
    if str(message.payload) == '0':
        print('Waiting on Player 2.')
    else:
        p2_int = str(message.payload)[2]
        if p2_int == '0':
            p2 = 'rock'
        elif p2_int == '1':
            p2 = 'paper'
        elif p2_int == '2':
            p2 = 'scissors'

        if str(message.payload)[0] == '1':
            p1_win += 1
            print('You win! Player 2 chose', p2)
        elif str(message.payload)[0] == '2':
            p2_win += 1
            print('You lose! Player 2 chose', p2)
        elif str(message.payload)[0] == '3':
            tie += 1
            print('It was a tie! You both chose', p2)
        print("P1 ", p1_win, "  P2 ", p2_win, "  Tie ", tie)


        inp = 0
        while True:
            inp = input('Rock(r) Paper(p) or Scissors(s)?')
            if inp != 'r' and inp != 'p' and inp != 's':
                print("Please enter 'r', 'p','s', or 'q'.")
            else:
                break

        if inp == 'r':
            player = 0
        elif inp == 'p':
            player = 1
        elif inp == 's':
            player = 2

        client.publish("ece180d/krish/p1_out", player, qos=1)
    
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

while True: # perhaps add a stopping condition using some break or something.
    pass # do your non-blocked other stuff here, like receive IMU data or something.
# use subscribe() to subscribe to a topic and receive messages.

# use publish() to publish messages to the broker.

# use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()