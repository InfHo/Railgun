from RPi import GPIO
from time import sleep

coil_num = 4

coil_pin = [4, 17, 22, 23]
coil_on_time = [30, 30, 30, 30]  # in ms
coil_delay = [5, 5, 5, 5]  # in ms

print("Initializing...")

GPIO.setmode(GPIO.BCM)

for i in range(coil_num):
    GPIO.setup(coil_pin[i], GPIO.OUT)
    GPIO.output(coil_pin[i], GPIO.LOW)  # turn relais off

print("Ready")

while True:
    cmd = input("> ")

    if cmd == "f":  # fire
        for i in range(coil_num):
            GPIO.output(coil_pin[i], GPIO.HIGH)  # turn relais on
            sleep(coil_on_time[i] / 1000)
            GPIO.output(coil_pin[i], GPIO.LOW)  # turn relais off
            sleep(coil_delay[i] / 1000)

    elif cmd.startswith("t "):  # test on time
        on_time = int(cmd.split()[1])
        GPIO.output(coil_pin[0], GPIO.HIGH)  # turn relais on
        sleep(on_time / 1000)
        GPIO.output(coil_pin[0], GPIO.LOW)  # turn relais off
        # sleep(coil_delay[i] / 1000)

    elif cmd.startswith("ta "):
        on_time = int(cmd.split()[1])
        delay = int(cmd.split()[2])
        for i in range(coil_num):
            GPIO.output(coil_pin[i], GPIO.HIGH)  # turn relais on
            sleep(on_time / 1000)
            GPIO.output(coil_pin[i], GPIO.LOW)  # turn relais off
            sleep(delay / 1000)

    
    elif cmd == "q":  # quit
        exit()

    else:
        print("Unknown command. To quit enter \"q\"")

