import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def measure_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.1)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    timeout_start = time.time()
    while GPIO.input(ECHO) == 0:
        if time.time() - timeout_start > 0.04:
            return None
    pulse_start = time.time()

    timeout_end = time.time()
    while GPIO.input(ECHO) == 1:
        if time.time() - timeout_end > 0.04:
            return None
    pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    if 2 <= distance <= 400:
        return distance
    else:
        return None

def cleanup():
    GPIO.cleanup()
