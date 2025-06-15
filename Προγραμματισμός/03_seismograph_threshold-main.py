from microbit import * 
import math 
import time 
import log 
 
log.set_labels('x', 'y', 'z', 'magnitude') 
 
# Configuration 
SAMPLE_RATE = 10  # 10 ms delay = 100 Hz sampling 
LOG_DURATION = 60  # Log for 60 seconds 
THRESHOLD = 0.02  # Threshold in g (adjust based on calibration) 

# Initialize variables for averaging
previous_magnitude = 0
alpha = 0.7  # Smoothing factor (0.0 to 1.0, higher = smoother)

# Threshold value
threshold = 0.1  # Adjust based on sensitivity needs

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
    
start_time = time.ticks_ms() 
 
# Main loop 
while time.ticks_diff(time.ticks_ms(), start_time) < LOG_DURATION * 1000: 
    x = accelerometer.get_x() 
    y = accelerometer.get_y() 
    z = accelerometer.get_z() 
 
    magnitude = calculate_magnitude(x, y, z) 
     
    # Apply thresholding 
    if abs(magnitude - 1.0) > threshold: 
        # Log data 
        log.add({ 
          'x': accelerometer.get_x(), 
          'y': accelerometer.get_y(), 
          'z': accelerometer.get_z(),  
          'magnitude': calculate_magnitude(x, y, z) 
        })
     
    sleep(SAMPLE_RATE) 
 
print("Done!") 