## Task 1

Here is a picture of the MCU working.
![IMG_5516](https://github.com/krishhshah/180DA-WarmUp/assets/95327144/ee6bd8e8-c613-435e-8ce9-dbc3c765e619)


Here are the IMU printouts.
<img width="1232" alt="Screenshot 2024-02-01 at 2 45 56 PM" src="https://github.com/krishhshah/180DA-WarmUp/assets/95327144/2a2199df-182b-4025-8c09-8f089db08efb">


The script for the Arudino is under '/IMU'

## Task 2

Here is the MCU connecting to WIFI.
<img width="1232" alt="Screenshot 2024-02-01 at 3 21 53 PM" src="https://github.com/krishhshah/180DA-WarmUp/assets/95327144/136de57d-9118-4469-bee4-809cf98e7fd0">


The script is under '/WIFI'

## Task 3

Here is the screenshot of the mqtt communciation between my Arduino and Computer.
<img width="983" alt="Screenshot 2024-02-01 at 3 52 33 PM" src="https://github.com/krishhshah/180DA-WarmUp/assets/95327144/d883c392-fe05-4f48-9bb4-f3d3d9ace091">


When the delay for sending messages was 8000 milliseconds, the lag was under .2 seconds.
When the delay for sending messages was 1000 milliseconds, the lag was around .35 seconds
When our frequency is higher, the lag gets a little longer.
We can combat this by keeping frequency low and also by doing all necessary algorithms before the message is sent so that the subscriber just has to receive the message and do nothing else to add to lag time.

The scripts are under '/MQTT'

## Task 4

The script is under '/Classification'


1) Yes, I can see the gravity acceleration while idle. Using the IMU I have figured out the +x,+y,+z values.

2) It looks as if the gyroscope values drift even when idle, either this is due to the senstiitvity of them or just simply the noise from the instrument itself. The acceleration values seem to be constant when it is idle. We can distinguish between idle and nonidle in a few ways. One is to take the average acceleration over a certain time and see how low it is. Another one would be to see if theres a difference in the current and previous values higher than an amount greater than the drift. ANother way is the one I will be using, it using instantaneous values ax, ay, and az and uses the following equation to see whether it is idle: ax^2 + ay^2 + az^2 = a^2. If a is between .97-1.03 (accounting for noise), we can say it is idle.

Here is the Confusion Matrix:
<img width="448" alt="Screenshot 2024-02-01 at 4 43 33 PM" src="https://github.com/krishhshah/180DA-WarmUp/assets/95327144/4b1f9f02-96f0-4c2a-88a0-2a6632397f0d">


3) When the Arduino is stationary the following values are usually displayed

"Sending IMU data to topic: Acceleration:  -0.07 -0.13 1.01	Gyroscope:  0.18 -0.24 -0.06"


When we push, we get these values

Sending IMU data to topic: Acceleration:  0.21 0.32 0.84	4.70 -2.26 -10.13

As such, we will classify a push with |gx|, |gy|, and |gz| > 1


For the lift we get this

Sending IMU data to topic: Acceleration:  -0.15 -0.84 0.57	Gyroscope:  -17.76 1.46 -2.01

As such, we will classify a lift with ay < -0.5 and gx < -10


My classifer works alright. It always picks up the movements, but sometimes causes false readings when I do something other than the 2 movements, this may be a result of the classifer not being specific enough. I use a decision tree of sorts with depth one, aka just a bunch of if else statements. The lift works quite well compared to the push. The push works, just not as well as lift.

4) I understood circular rotation as twisting the arduino as if ur twisting a doorknob. The way I classified this gesture is by seeing if the arduino hits 90, 180, 270, and 360 degrees. Once these degrees have been met, we can consitute that as a rotation. I added a timer so that the circular rotation must be done within a certain 5 second frame.

I was able to use the same features as before but in a compeltely different way.
I was able to easily track a circular rotation as long as it was d=one during the time frame of 5 seconds. I used the AZ and AY features.
