from microbit import *
import radio

radio.on()
radio.config(group=1)  # Same channel as transmitter

# Servo motor settings
SERVO_MIN_PULSE = 25
SERVO_MAX_PULSE = 125
SERVO_MIN_ANGLE = 60
SERVO_MAX_ANGLE = 120

servoPin = pin0
servoPin.set_analog_period(20)

def SetServo(servoPin, angle):
    angle = max(0, min(180, angle))  # Clamp angle between 0-180
    pulse = (SERVO_MAX_PULSE - SERVO_MIN_PULSE) * angle / 180 + SERVO_MIN_PULSE
    servoPin.write_analog(pulse)

def normalize_to_servo_angle(magnitude, min_value=0, max_value=10):
    magnitude = max(min_value, min(max_value, magnitude))
    return int((magnitude - min_value) / (max_value - min_value) * (SERVO_MAX_ANGLE - SERVO_MIN_ANGLE) + SERVO_MIN_ANGLE)

# Initialize servo to center position
SetServo(servoPin, (SERVO_MIN_ANGLE + SERVO_MAX_ANGLE) // 2)

while True:
    message = radio.receive()
    if message:
        try:
            magnitude = int(message)
            print("Received:", magnitude)

            # Convert to servo angle
            servo_angle = normalize_to_servo_angle(magnitude)
            SetServo(servoPin, servo_angle)
        except ValueError:
            pass  # Ignore invalid data

    sleep(500)  # Adjust for smoother response
