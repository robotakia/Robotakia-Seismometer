from microbit import *

while True:
    # Λήψη τιμών από τον επιταχυνσιόμετρο
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()
    
    # Εμφάνιση των τιμών στον σειριακό για λεπτομέρειες
    print("X:", x, "Y:", y, "Z:", z)
    
    # Εμφάνιση των τιμών στον άξονα X στην οθόνη
    display.scroll("X: {}".format(x))
    sleep(1000)
    display.scroll("Y: {}".format(y))
    sleep(1000)
    display.scroll("Z: {}".format(z))
    sleep(1000)

