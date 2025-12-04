Measuring Height Using Ultrasonic Sensor and Raspberry Pi

  Hardware:
  
    An HC-SR04 ultrasonic sensor is mounted at a fixed height (about 200 cm) above the ground.
    
    The sensor sends out high-frequency sound waves (ultrasound) that bounce off the top of a person’s head and return to the sensor.
    
    The sensor measures the time it takes for the sound waves to travel to the person and back.
    
    This time is converted into a distance measurement (in centimeters).

Software:

    A Python program running on the Raspberry Pi controls the sensor, triggering the ultrasonic pulse and listening for the echo.
    
    The program takes multiple distance readings to improve accuracy and filters out invalid or inconsistent measurements.
    
    It calculates the person’s height by subtracting the measured distance from the sensor’s fixed mounting height.
    
    The result is displayed on an LCD screen attached to the Raspberry Pi.
    
    The software logs all measurements and errors for debugging and reliability.
    
    If no valid reading is detected, it informs the user gracefully.

The system measures how far the top of a person’s head is from the sensor, then subtracts this distance from the sensor’s mounting height to calculate the person’s height accurately.
