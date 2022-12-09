# BassBot
A single-string bass playing robot that changes the pitch by varying tension in the string.

### Functionality
The robot has a fundamentally different pitch changing mechanism. Instead of a fretting hand, it changes pitch by changing the tuning of the string. In addition, the bot has a plucking mechanism and a damping mechanism which adds control over the notes and also adds an additional capability of playing ghost notes. It uses 3 motors - 1 Dynamixel for changing the tuning and 2 steppers, one each for fretting and damping mechanism. Steppers are controlled using Arduino, whereas the Dynamixel is controlled using dynamixel_sdk. The whole system is controlled using a raspberry pi.


### Implementation
Execute bassbot.py to play notes from notes.csv on the bassBot.

Demo video at Georgia Tech Center for Music Technology: https://youtu.be/B3lX4Uc-3wo
