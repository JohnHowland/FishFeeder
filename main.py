import RPi.GPIO as GPIO
import time
import peripherals.button as btn

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

sw = btn.button(17)

try:  
    while True:  
         time.sleep(10.0)
         GPIO.output(4, 1)
         
         motorRunning = True
         mm = False
         while motorRunning is True: 
             val = sw.buttonIn

             if val == 1:
                 print("switch pressed")
                 mm = True

             if val == True and mm == True:
                print("switch released")
                motorRunning = False
                GPIO.output(4, 0)








#        GPIO.output(4, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
#        time.sleep(2.0)                 # wait half a second  
#        if GPIO.input(4):  
#            print("LED just about to switch off" )
#        GPIO.output(4, 0)         # set GPIO24 to 0/GPIO.LOW/False  
#        time.sleep(2.0)                 # wait half a second  
#        if not GPIO.input(4):  
#            print("LED just about to switch on" ) 

except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
    GPIO.cleanup()                 # resets all GPIO ports used by this program