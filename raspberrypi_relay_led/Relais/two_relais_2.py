# working

import RPi.GPIO as GPIO
import time



GPIO.setmode(GPIO.BCM) # GPIO Nummern statt Board Nummern

#If true it will give out warning
GPIO.setwarnings(False)

def relais_runner(x, t):
    RELAIS_1_GPIO = x
    GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Modus zuweisen
    GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # aus
    GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # an

    time.sleep(t)

    GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # aus

relais_runner(4,2)
relais_runner(17,2)
