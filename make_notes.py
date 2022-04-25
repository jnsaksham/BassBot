input numpy as np

# Delay is added by the rotation of servo motor. 
# Calculate this delay and adjust in the final code.
# Define everything using an input metronome value with type (whole, half, quarter, eighth, sixteenth) as note type

#### Note definition (position, duration, style)
# Every note should have an onset time and a rest (post offset) time for the servo to adjust-
## Servo should reach the position before the onset time
## Exactly at the onset time, stepper should pluck
## Damper should damp at the offset time

arduino_pos_per_rev = 6400

def note(position, dur, style):
# Convert position to pitch eventually
	pass


