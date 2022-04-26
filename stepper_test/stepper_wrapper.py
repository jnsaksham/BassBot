import numpy as np
from pymata4 import pymata4
import time

board = pymata4.Pymata4()
num_steps = 6400
vel = 360
pins = [2,3]


try:
    while 1:
        num_steps = int(input("Enter goal position\n"))

        board.set_pin_mode_stepper(num_steps, pins)
        ts1 = time.time()
        board.stepper_write(vel, num_steps)
        ts2 = time.time()
        time.sleep(1)
        ts3 = time.time()
        print (ts1, ts2, ts3)
        print ('differences: ', ts2-ts1, ts3-ts2)
    # board.stepper_write(vel, -num_steps)
    # time.sleep(0.5)

except KeyboardInterrupt:
    board.shutdown()
