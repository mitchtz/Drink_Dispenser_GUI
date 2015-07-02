#Test file for function that control gpio pins on rpi

import RPi.GPIO as GPIO #To interface with Raspberry Pis GPIO pins
import time #To sleep program
#Get pin to test on
pin = input("Pin to interface with: ")

done = False
while not done:
	#Get time in seconds to run pump
	pump_time = input("Time to pump (in seconds): ")
	#Check for done or exit
	if (pump_time == "done") or (pump_time == "exit"):
		done = True
	#Otherwise run pump
	else:
		#Setup output pin, default turn on is low voltage
		GPIO.setup(pin, GPIO.OUT)
		
	    #Set GPIO pin to high voltage
	    #Should turn pump on
		GPIO.output(pin, True)

	    #Wait specified time before turning off
		time.sleep(int(pump_time))

	    #Set GPIO pin to low voltage
		#Should turn pump off
		GPIO.output(pin, False)