from microbit import *
import math
import radio

radio.on()
radio.config(group=1)  # Set a unique channel

alpha = 0.7  # Smoothing factor
previous_magnitude = 0

def calculate_smoothed_magnitude(x, y, z):
    global previous_magnitude
    magnitude = math.sqrt(x**2 + y**2 + z**2) / 1024  # Normalize to 'g'
    smoothed_magnitude = alpha * magnitude + (1 - alpha) * previous_magnitude
    previous_magnitude = smoothed_magnitude
    return int((smoothed_magnitude * 10) % 10)  # Scale to 0-9

while True:
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()

    magnitude = calculate_smoothed_magnitude(x, y, z)
    
    radio.send(str(magnitude))  # Send magnitude over radio
    print("Sent:", magnitude)

    sleep(500)  # Adjust sampling rate

