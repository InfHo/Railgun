# working

import RPi.GPIO as GPIO
import time



GPIO.setmode(GPIO.BCM) # GPIO Nummern statt Board Nummern

#If true it will give out warning
GPIO.setwarnings(False)


RELAIS_1_GPIO = 4
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Modus zuweisen
GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # aus

for i in range(5):
    GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # an

    #time.sleep(0.005)
    time.sleep(1)
    GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # aus

