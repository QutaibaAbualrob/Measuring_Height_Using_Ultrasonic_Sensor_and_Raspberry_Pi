import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def measure_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)

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

def measure_height(sensor_height_cm, samples=10, sample_delay=0.02, floor_margin=12, min_valid=3):
    """
    Takes multiple ultrasonic distance readings.
    Returns (height, stats) or (None, stats) if not enough valid samples.
    """
    values = []

    for _ in range(samples):
        d = measure_distance()
        if d is not None and d <= sensor_height_cm - floor_margin:
            values.append(d)
        time.sleep(sample_delay)

    stats = {
        "valid_samples": len(values),
        "raw_values": values,
    }

    if len(values) < min_valid:
        return None, stats

    avg_distance = sum(values) / len(values)
    height = sensor_height_cm - avg_distance

    return height, stats

def cleanup():
    GPIO.cleanup()
