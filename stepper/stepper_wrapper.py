import numpy as np
from pymata4 import pymata4
import time

num_steps = 512
pins = [2,3]
board = pymata4.Pymata4()

board.set_pin_mode_stepper(num_steps, pins)

while True:
    board.stepper_write(21, num_steps)
    time.sleep(1)
    board.stepper_write(21, -512)
    time.sleep(0.5)