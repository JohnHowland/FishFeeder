import string
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import logging

MAX_DEBOUNCE_NUMBER = 15

class button:
    def __init__(self, pinNumber):
        GPIO.setup(pinNumber, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.pinNumber = pinNumber
        self.highCount = 0
        self.lowCount = 0
        logging.debug("Init button: " + str(pinNumber))

    def buttonIn(self):
        currentState = GPIO.input(self.pinNumber)

        if currentState == GPIO.LOW and self.highCount > MAX_DEBOUNCE_NUMBER and self.lowCount == 0:
            self.lowCount = 0
            logging.debug("Button " + str(self.pinNumber) + " pressed.")
            ret = 1
        else:
            if currentState == GPIO.LOW:
                self.highCount = 0
            ret = 0

        if currentState == GPIO.HIGH:
#            logging.debug("registered push")
            self.highCount += 1
            self.lowCount = 0
        else:
            self.lowCount += 1
            self.highCount = 0

        return ret
        
        


if __name__ == '__main__':

    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
#    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
#    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#    GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    button16 = button(16)
    button18 = button(18)
    button22 = button(22)
    button32 = button(32)


    while True: # Run forever
        if button16.buttonIn() == 1:
            print("Button 16 was pushed!")

        if button18.buttonIn() == 1:
            print("Button 18 was pushed!")

        if button22.buttonIn() == 1:
            print("Button 22 was pushed!")

        if button32.buttonIn() == 1:
            print("Button 32 was pushed!")