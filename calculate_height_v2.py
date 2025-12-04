import time
import measure_range
import height_lcd
import debug_log

log = debug_log.log

# ---------- Settings ----------
SENSOR_HEIGHT_CM = 204  # Your sensor mounting height (cm)
SAMPLES = 9
SAMPLE_DELAY = 0.05
FLOOR_MARGIN = 12
MIN_VALID = 3
UPDATE_INTERVAL = 0.6      # Seconds between LCD updates
STABLE_THRESHOLD = 0.5     # cm difference to consider stable
STABLE_COUNT_REQUIRED = 2  # Number of stable readings before final display

GREETING = "Hello !"
NO_TARGET_MSG = "No target"
MEASURING_MSG = "Measuring..."

def main():
    log.info("Program started")
    height_lcd.init_lcd()
    height_lcd.show_message("Starting...", "Please wait")
    time.sleep(1.0)

    last_height = None
    stable_count = 0

    try:
        while True:
            height, stats = measure_range.measure_height(
                sensor_height_cm=SENSOR_HEIGHT_CM,
                samples=SAMPLES,
                sample_delay=SAMPLE_DELAY,
                floor_margin=FLOOR_MARGIN,
                min_valid=MIN_VALID
            )

            log.debug(f"Raw samples: {stats['raw_values']}, valid_samples: {stats['valid_samples']}")

            if height is None:
                # No valid reading
                log.warning("No valid height measurement obtained")
                height_lcd.clear()
                height_lcd.show_message("Distance:", NO_TARGET_MSG)
                last_height = None
                stable_count = 0
            else:
                # Valid height measurement
                log.info(f"Measured height: {height:.2f} cm")
                if last_height is not None and abs(height - last_height) <= STABLE_THRESHOLD:
                    stable_count += 1
                else:
                    stable_count = 0

                if stable_count >= STABLE_COUNT_REQUIRED:
                    height_lcd.show_height(height, GREETING)
                else:
                    height_lcd.show_message(MEASURING_MSG, f"{height:.2f} cm")

                last_height = height

            time.sleep(UPDATE_INTERVAL)

    except KeyboardInterrupt:
        log.info("Measurement stopped by user (KeyboardInterrupt)")
    except Exception as e:
        log.error(f"Unexpected exception: {e}")
    finally:
        height_lcd.shutdown()
        measure_range.cleanup()
        log.info("Program ended")

if __name__ == "__main__":
    main()
