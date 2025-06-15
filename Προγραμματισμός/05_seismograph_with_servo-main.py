from microbit import * 
import math 
import time 
import log 

log.set_labels('x', 'y', 'z', 'magnitude') 

# =========== Servo ===========
SERVO_MIN_PULSE = 25 # theoretical 50, measured 23
SERVO_MAX_PULSE = 125 # theoretical 100, measured 127

servoPin = pin0
servoPin.set_analog_period(20)

# Define servo limits for drawing
SERVO_MIN_ANGLE = 60  # Minimum angle for pen movement
SERVO_MAX_ANGLE = 120  # Maximum angle for pen movement

def SetServo(servoPin, angle):
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180
    
    pulse = (SERVO_MAX_PULSE - SERVO_MIN_PULSE) * angle / 180 + SERVO_MIN_PULSE
    servoPin.write_analog(pulse)
    
# Configuration 
SAMPLE_RATE = 500  # 10 ms delay = 100 Hz sampling 
LOG_DURATION = 60  # Log for 60 seconds 

# Initialize variables for averaging
previous_magnitude = 0
alpha = 0.7  # Smoothing factor (0.0 to 1.0, higher = smoother)

# Threshold value
threshold = 0.5  # Adjust based on sensitivity needs

# Function to calculate magnitude of acceleration 
def calculate_magnitude(x, y, z): 
    return math.sqrt(x**2 + y**2 + z**2) / 1000  # Convert to g-force 

def calculate_smoothed_magnitude(x, y, z): 
    global previous_magnitude 
    # Calculate magnitude 
    magnitude = math.sqrt(x**2 + y**2 + z**2) / 1024  # Normalize to 'g' 
 
    # Apply moving average (Exponential Smoothing) 
    smoothed_magnitude = alpha * magnitude + (1 - alpha) * previous_magnitude 
    previous_magnitude = smoothed_magnitude 
     
    # Return smoothed magnitude (scaled to 0-9 for simplicity) 
    return (smoothed_magnitude * 10) % 10 

# Function to normalize magnitude to servo angle (0-180 degrees)
def normalize_to_servo_angle(magnitude, min_value=0, max_value=10):
    # Clamp magnitude to the expected range
    magnitude = max(min_value, min(max_value, magnitude))

    # Normalize to the limited servo range (SERVO_MIN_ANGLE to SERVO_MAX_ANGLE)
    return int((magnitude - min_value) / (max_value - min_value) * (SERVO_MAX_ANGLE - SERVO_MIN_ANGLE) + SERVO_MIN_ANGLE)

start_time = time.ticks_ms() 

# Initialize servo to center position
SetServo(servoPin, (SERVO_MIN_ANGLE + SERVO_MAX_ANGLE) // 2)

# Main loop 
while time.ticks_diff(time.ticks_ms(), start_time) < LOG_DURATION * 1000: 
    x = accelerometer.get_x() 
    y = accelerometer.get_y() 
    z = accelerometer.get_z() 
 
    magnitude = calculate_smoothed_magnitude(x, y, z) 
    print(magnitude)
    # Normalize magnitude to servo angle
    servo_angle = normalize_to_servo_angle(magnitude)
    print(servo_angle)
    SetServo(servoPin, servo_angle) # servo pin and angle
    
    # Apply thresholding 
    if abs(magnitude - 1.0) > threshold: 
        # Log data 
        log.add({ 
          'x': accelerometer.get_x(), 
          'y': accelerometer.get_y(), 
          'z': accelerometer.get_z(),  
          'magnitude': calculate_smoothed_magnitude(x, y, z) 
        })
     
    sleep(SAMPLE_RATE) 
 
print("Done!") 