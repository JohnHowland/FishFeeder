import RPi.GPIO as GPIO
import time
import peripherals.button as btn
import os
import logging


def getStatusIfUpdated():
    global StatusFileTime, StatusFile, runStatus, lastRunStamp

    curfileTime = os.path.getmtime(StatusFile)
#    logging.debug(f"curfileTime: {curfileTime}")
    if StatusFileTime != curfileTime:
        logging.debug("The STATUS file time is different")
        StatusFileTime = curfileTime

        try:
            fp = open(StatusFile, "r")
            line = fp.readline()
            logging.debug(f"line: {line}")
            if "start" in line:
                runStatus = True
                logging.debug("Run status to TRUE")
            elif "stop" in line:
                runStatus = False
                lastRunStamp = 0.0
                logging.debug("Run status to FALSE")
            else:
                logging.debug("ERROR parsing the status file")
            fp.close()
        except:
            logging.debug("Error occured in trying to open status file")

        return True
    else:
        return False


def getUpatedFile():
    global UpdateFileTime, UpdateFile, hoursBetweenCycles, cycleCount

    curfileTime = os.path.getmtime(UpdateFile)
#    logging.debug(f"curfileTime: {curfileTime}")
    if UpdateFileTime != curfileTime:
        logging.debug("The UPDATE file time is different")
        UpdateFileTime = curfileTime

        try:
            fp = open(UpdateFile, "r")
            line = fp.readline()
            logging.debug(f"line: {line}")
            try:
                line_strip = line.split('-')
                hoursBetweenCycles = float(line_strip[0])*60*60
                cycleCount = int(line_strip[1])
            except:
                logging.debug("Error with parsing line")
        
            fp.close()
        except:
            logging.debug("Error occured in trying to open status file")


        return True
    else:
        return False


TEST = True

root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG) # or whatever
handler = logging.FileHandler('test.log', 'w', 'utf-8') # or whatever
handler.setFormatter(logging.Formatter('%(name)s %(message)s')) # or whatever
root_logger.addHandler(handler)

runStatus = False
cycleCount = 0
hoursBetweenCycles = 12*60*60           #in seconds

StatusFile = "/home/pi/dev/fishFeederVars/status.txt"
StatusFileTime = None
UpdateFile = "/home/pi/dev/fishFeederVars/update.txt"
UpdateFileTime = None
lastRunStamp = 0.0

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

sw = btn.button(17)

try:  
    while True: 
        time.sleep(5.0) 
        if runStatus is True: 
             
             if time.monotonic() - lastRunStamp > hoursBetweenCycles:
                 lastRunStamp = time.monotonic()
  
                 for i in range(cycleCount):
                     logging.debug("Motor on")
                     GPIO.output(4, 1)
                     motorRunning = True
                     mm = False
                     while motorRunning is True: 
                         
                        if TEST is False:
                            val = sw.buttonIn()
                        else:
                            val = 1

                        if val == 1:
                             logging.debug("switch pressed")
                             mm = True

                        if val == True and mm == True:
                            logging.debug("switch released")
                            motorRunning = False
                            GPIO.output(4, 0)
                            logging.debug("motor off")

        else:
            pass

        getStatusIfUpdated()
        getUpatedFile()



except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()                 # resets all GPIO ports used by this program


