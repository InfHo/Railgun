#Blinking red LED
#python 3.5.3 for RaspberryPi3

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#If true it will give out warning
GPIO.setwarnings(False)

#here connected on GPIO18
ledPin = 18
GPIO.setup(ledPin, GPIO.OUT)

GPIO.output(ledPin,GPIO.HIGH)
time.sleep(5)
GPIO.output(ledPin, GPIO.LOW)

