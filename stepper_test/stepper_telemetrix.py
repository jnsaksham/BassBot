import sys
import time
import telemetrix

pin = 2

# Callback data indices
CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3

def the_callback(data):
	date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[CB_TIME]))
	print ('Pin Mode: ', data[CB_PIN_MODE])
	print ('Pin: ', data[CB_PIN])
	print ('Value: ', data[CB_VALUE])
	print ('Time stamp: ', date)
	
def digital_in(my_board, pin):
	my_board.set_pin_mode_digital_input(pin, the_callback)
	try:
		while True:
			time.sleep(0.0001)
	except KeyboardInterrupt:
		my_board.shutdown()
		sys.exit(0)

board = telemetrix.Telemetrix()

try:
	digital_in(board, pin)
except KeyboardInterrupt:
	board.shutdown()
	sys.exit(0)
