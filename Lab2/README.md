## Task 4

### 1) ring.py

Our team conssited of nick nhien, matthew fiorella and i. we created a ring of counter increments in the file ring.py.
Attached is a screenshot of my terminal.

<img width="455" alt="Screenshot 2024-01-18 at 3 28 36 PM" src="https://github.com/krishhshah/180DA-WarmUp/assets/95327144/1b5ad2a2-9c5a-4b29-abd3-661458b081d2">

Using MQTT, we can create a multipoint communciation network. We can craete rings, broadcasts, etc. 

Using MQTT, it may be hard to ensure security. Addiitonally, it seems a little hard to scale this network beyond an amount needed for this class. With each scaled mamebr it wasn't too bad but I can see how it can get exponentially complex with more.

A reasonable communications lag time would probaly be the latency of the server. We tested under .5 seconds and it seemed to be okay. 

I think this is a very decent way to transmit data as long as we aren't concerned about security and as such this can be preferable.

### 2) speech.py

In distinguishing separate words, it is pretty good.
When testing similar sounding words, the performacne sometimes takes a hit. For example, when testing sound and found, the recognizer would classify found as sound. Same thing with fee and sea.
Phrases seemed to work okay. I used a tongue twister on the program and it got it perfectly. Sally sells seashells by the seashore. It is a little slower though. The phrase seems to be a good thing for error-correction.
Working in the lab was horrible. Everytime there was some background words, the recognizer would take a really long time. Sometimes it would even say it couldn't figure the phrase out. We can probably only look for certain phrases or use a proper microphone.

a) In the project, we can use the speech program to say certain words like defuse or arm for our bomb explosion game. We can also have other phrases that can solve puzzles.
b) From a coding standpoint, we don't want our speech recognition to be too complex. Becasue the words and phrases we may use in our game is not stuff that is commonly said, we can reasonably expect our recognition to be quite simple.
c) In our project we need an accurate recognition quite quickly. Since this game may be based on a time trial, any loss in time would be detrimental to gameplay.
d) Yes, we will probbaly need a microphone and somewhat quiet atmosphere to have it work well enough.


## References
https://pypi.org/project/SpeechRecognition/1.2.3/
