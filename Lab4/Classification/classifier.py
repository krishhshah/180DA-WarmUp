import paho.mqtt.client as mqtt
import numpy as np
import time
import json

counter = 0
window = []
up= False
down = False
left = False
right = False
interval = 5
start = time.time()
end = time.time()

# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ece180d/ks", qos=1)

# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

# The default message callback.
# (you can create separate callbacks per subscribed topic)
def on_message(client, userdata, message):
    global start
    global end
    global window
    global up
    global right
    global left
    global down

    message.payload = message.payload.decode("utf-8")
    # print('Received message: "' + str(message.payload) + '" on topic "' +
    #     message.topic + '" with QoS ' + str(message.qos))
    imu = json.loads(message.payload)
    g_acceleration = imu["ax"]**2 + imu["ay"]**2 + imu["az"]**2
    g_acceleration = g_acceleration**(.5)
    # window.append(imu)
    # if len(window) > 10:
    #     window.pop()
    # for i in range(9):
    #     if window[i+1]["ay"] > .9
    #     if window[i+1]["ay"] > .9
    #     if window[i+1]["ay"] > .9
    #     if window[i+1]["ay"] > .9

    end = time.time()
    if end - start > interval:
        start = time.time()

    elif imu["ay"] > .8:
        left = True
    elif imu["ay"] < -0.8:
        right = True
    elif imu["az"] > .8:
        up = True
    elif imu["az"] < -0.8:
        down = True
    if up and down and left and right:
        up = False
        down = False
        left = False
        right = False
        print("circular rotation")
    # print(g_acceleration)
    elif imu["gx"] > 1 and imu["gy"] > 1 and (imu["gz"] > 1 or imu["gz"] < 1):
        print("push")
    elif imu["ay"] < -0.5 and imu["gx"] < -10:
        print("lift")
    elif g_acceleration > 1.03 or g_acceleration < .97:
        print("not-idle")
    else:
        print("idle")

    
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
client.connect_async('broker.hivemq.com')
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