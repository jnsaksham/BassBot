import numpy as np
import csv
import time
import util

# Define everything using an input metronome value with type (whole, half, quarter, eighth, sixteenth) as note type

tempo = 60
ibi = 60/tempo

# Arduino operation times
durComm = 0.05 # Arduino, py communication lag
durRotate = 0.1 # Motor rotation time before it plucks

# Note information
positions = np.array([0, 500, 2000, 0, 3000, 0, 2000, 0])
num_notes = len(positions)
songDur = len(positions)*ibi
# styles = np.array(['n', 'n', 's', 's', 'n', 's', 's', 'n'])
styles = np.array(['n', 's', 'n', 's', 's', 'n', 'n', 'n'])
# styles = np.full(num_notes, 'n')
dampNote = np.array([0, 0, 0, 0, 0, 0, 0, 0])

noteDurations = np.full(num_notes, 0.2)

util.playSong(tempo, songDur, positions, noteDurations, styles, dampNote, durComm, durRotate)