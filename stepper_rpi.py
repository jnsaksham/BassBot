from time import sleep
import RPi.GPIO as GPIO

DIR = 23
STEP = 24
ENABLE=25
CW = 1
CCW = 0
STEPS_PER_REVOLUTION = 48

GPIO.setmode(GPIO.BCM)
print("Setting up GPIO Pins")
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP,GPIO.OUT)
GPIO.setup(ENABLE, GPIO.OUT)
print("Setting DIR to CW")
GPIO.output(DIR,CW)
print("Setting ENABLE")
GPIO.output(ENABLE, GPIO.LOW)
delay = 0.2
try:
    for x in range(STEPS_PER_REVOLUTION):
        if x%10 == 0:
            print(f"STEP {x}")
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)

    sleep(0.5)
    GPIO.output(DIR, CCW)
    print("Changing direction")
    for x in range(STEPS_PER_REVOLUTION):
        print("LL")
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)

    GPIO.cleanup()

except:
    GPIO.cleanup()
