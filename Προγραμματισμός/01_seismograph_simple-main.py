from microbit import * 
import math 
import time 
import log 
 
log.set_labels('x', 'y', 'z', 'magnitude') 
 
# Configuration 
SAMPLE_RATE = 10  # 10 ms delay = 100 Hz sampling 
LOG_DURATION = 60  # Log for 60 seconds 
THRESHOLD = 0.02  # Threshold in g (adjust based on calibration) 
 
# Function to calculate magnitude of acceleration 
def calculate_magnitude(x, y, z): 
    return math.sqrt(x**2 + y**2 + z**2) / 1000  # Convert to g-force 
 
start_time = time.ticks_ms() 
 
# Main loop 
while time.ticks_diff(time.ticks_ms(), start_time) < LOG_DURATION * 1000: 
    x = accelerometer.get_x() 
    y = accelerometer.get_y() 
    z = accelerometer.get_z() 
 
    # Log data 
    log.add({ 
      'x': accelerometer.get_x(), 
      'y': accelerometer.get_y(), 
      'z': accelerometer.get_z(),  
      'magnitude': calculate_magnitude(x, y, z) 
    }) 
     
    sleep(SAMPLE_RATE) 
 
print("Done!") 