import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# Ρύθμιση της σειριακής θύρας (Τροποποίησε το COM3 αν χρειάζεται)
SERIAL_PORT = "COM3"  # Στα Windows μπορεί να είναι COMx, σε Mac/Linux "/dev/ttyUSB0" ή "/dev/ttyACM0"
BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

# Δημιουργία παραθύρου
fig, ax = plt.subplots()
x_data = deque(maxlen=100)
y_data = deque(maxlen=100)
line, = ax.plot([], [], 'r')

def update(frame):
    if ser.in_waiting > 0:
        data = ser.readline().decode().strip()
        try:
            value = float(data)
            x_data.append(frame)
            y_data.append(value)
            line.set_data(list(x_data), list(y_data))
            ax.relim()
            ax.autoscale_view()
        except ValueError:
            pass

ani = animation.FuncAnimation(fig, update, interval=500, save_count=100)
plt.xlabel("Χρόνος")  # X-axis label
plt.ylabel("Magnitude")  # Y-axis label
plt.title("Live Δεδομένα από Micro:bit")  # Title

plt.show()