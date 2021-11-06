# last version with 4 relais

import RPi.GPIO as GPIO
import time



GPIO.setmode(GPIO.BCM) # GPIO Nummern statt Board Nummern

#If true it will give out warning
GPIO.setwarnings(False)

def relais_runner(x, t):
    RELAIS_1_GPIO = x
    GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Modus zuweisen
    GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # an
    time.sleep(time_1)
    GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # aus

# 0.02 ohne extrapause funzt gut

time_1 = 0.02

# GPIO 4
n = 4
GPIO.setup(n, GPIO.OUT)
GPIO.output(n, GPIO.HIGH)
time.sleep(time_1)
GPIO.output(n, GPIO.LOW)
#time.sleep(time_1)
# GPIO 17
m = 17
GPIO.setup(m, GPIO.OUT)
GPIO.output(m, GPIO.HIGH)
time.sleep(time_1)
GPIO.output(m, GPIO.LOW)

#time.sleep(time_1)
# GPIO 22
o = 22
GPIO.setup(o, GPIO.OUT)
GPIO.output(o, GPIO.HIGH)
time.sleep(time_1)
GPIO.output(o, GPIO.LOW)
#time.sleep(time_1)

# GPIO 23
o = 23
GPIO.setup(o, GPIO.OUT)
GPIO.output(o, GPIO.HIGH)
time.sleep(time_1)
GPIO.output(o, GPIO.LOW)








print("Zeit:"+str(time_1)+ "s")

