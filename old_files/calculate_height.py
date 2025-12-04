import time
import measure_range

SENSOR_HEIGHT_CM = 190  # sensor base

try:
    while True:
        dist = measure_range.measure_distance()
        if dist is not None:
            height = SENSOR_HEIGHT_CM - dist
            print(f"Distance from sensor: {dist} cm")
            print(f"Calculated height: {height} cm")
        else:
            print("No valid reading")
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    measure_range.cleanup()
