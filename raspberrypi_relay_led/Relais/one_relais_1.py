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


time_1 = 0.1
#relais_runner(4,2)
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, GPIO.HIGH)
time.sleep(time_1)
GPIO.output(4, GPIO.LOW)
#relais_runner(17,2)

print("Zeit:"+str(time_1)+ "s")
