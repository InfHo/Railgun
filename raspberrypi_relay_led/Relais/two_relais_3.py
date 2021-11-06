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

#relais_runner(4,2)
#relais_runner(17,2)

def relais_looper(relais_list, time, number):
        for i in range(number):
            for i in relais_list:
	        relais_runner(i,time)


relais_looper([4,17],1,5)

relais_looper([4,17],0.5,5)

#relais_looper([4,17],0.1,5)

#relais_looper([4,17],0.05,5)

#relais_looper([4,17],0.01,5)

