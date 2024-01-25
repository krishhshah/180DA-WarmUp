import paho.mqtt.client as mqtt
import numpy as np
import time

p1_recieved = False
p2_recieved = False
p1 = 4
p2 = 4
# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ece180d/krish/p1_out", qos=1)
    client.subscribe("ece180d/krish/p2_out", qos=1)

# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

# The default message callback.
# (you can create separate callbacks per subscribed topic)
def on_message(client, userdata, message):
    global p1_recieved
    global p2_recieved
    global p1
    global p2

    message.payload = message.payload.decode("utf-8")
    print('Received message: "' + str(message.payload) + '" on topic "' +
        message.topic + '" with QoS ' + str(message.qos))
    
    if message.topic == 'ece180d/krish/p1_out':
        p1_recieved = True
        p1 = int(message.payload)
        if not p2_recieved:
            client.publish("ece180d/krish/p1_in", 0, qos=1)
    elif message.topic == 'ece180d/krish/p2_out':
        p2_recieved = True
        p2 = int(message.payload)
        if not p1_recieved:
            client.publish("ece180d/krish/p2_in", 0, qos=1)
    
    if p1_recieved and p2_recieved:
        if p1 == p2:
            client.publish("ece180d/krish/p2_in", f'3{p1}{p2}', qos=1)
            client.publish("ece180d/krish/p1_in", f'3{p1}{p2}', qos=1)
        elif (p1 - p2) == 2:
            client.publish("ece180d/krish/p2_in", f'2{p1}{p2}', qos=1)
            client.publish("ece180d/krish/p1_in", f'2{p1}{p2}', qos=1)
        elif (p1 - p2) == -2:
            client.publish("ece180d/krish/p2_in", f'1{p1}{p2}', qos=1)
            client.publish("ece180d/krish/p1_in", f'1{p1}{p2}', qos=1)
        elif p1 > p2:
            client.publish("ece180d/krish/p2_in", f'1{p1}{p2}', qos=1)
            client.publish("ece180d/krish/p1_in", f'1{p1}{p2}', qos=1)
        elif p2 > p1:
            client.publish("ece180d/krish/p2_in", f'2{p1}{p2}', qos=1)
            client.publish("ece180d/krish/p1_in", f'2{p1}{p2}', qos=1)
        p1_recieved = False  
        p2_recieved = False


    
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

client.publish("ece180d/krish/p2_in", 'start', qos=1)
client.publish("ece180d/krish/p1_in", 'start', qos=1)

while True: # perhaps add a stopping condition using some break or something.
    pass # do your non-blocked other stuff here, like receive IMU data or something.
# use subscribe() to subscribe to a topic and receive messages.

# use publish() to publish messages to the broker.

# use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()