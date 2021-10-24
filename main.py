import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

try:  
    while True:  
        GPIO.output(7, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
        time.sleep(2.0)                 # wait half a second  
        if GPIO.input(7):  
            print("LED just about to switch off" )
        GPIO.output(7, 0)         # set GPIO24 to 0/GPIO.LOW/False  
        time.sleep(2.0)                 # wait half a second  
        if not GPIO.input(7):  
            print("LED just about to switch on" ) 

except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
    GPIO.cleanup()                 # resets all GPIO ports used by this program