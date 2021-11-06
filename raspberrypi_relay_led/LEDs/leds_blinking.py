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

for i in range(15):
        print("LED turning on")
        GPIO.output(ledPin,GPIO.HIGH)
        time.sleep(0.5)
        print("LED turning off")
        GPIO.output(ledPin, GPIO.LOW)
        time.sleep(0.5)

