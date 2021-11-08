import RPi.GPIO as GPIO
import time
import peripherals.button as btn
import os


def getStatusIfUpdated():
    global StatusFileTime, StatusFile, runStatus, lastRunStamp

    curfileTime = os.path.getmtime(StatusFile)
#    print(f"curfileTime: {curfileTime}")
    if StatusFileTime != curfileTime:
        print("The STATUS file time is different")
        StatusFileTime = curfileTime

        try:
            fp = open(StatusFile, "r")
            line = fp.readline()
            print(f"line: {line}")
            if "start" in line:
                runStatus = True
                print("Run status to TRUE")
            elif "stop" in line:
                runStatus = False
                lastRunStamp = 0.0
                print("Run status to FALSE")
            else:
                print("ERROR parsing the status file")
            fp.close()
        except:
            print("Error occured in trying to open status file")



        return True
    else:
        return False


def getUpatedFile():
    global UpdateFileTime, UpdateFile, hoursBetweenCycles, cycleCount

    curfileTime = os.path.getmtime(UpdateFile)
#    print(f"curfileTime: {curfileTime}")
    if UpdateFileTime != curfileTime:
        print("The UPDATE file time is different")
        UpdateFileTime = curfileTime

        try:
            fp = open(UpdateFile, "r")
            line = fp.readline()
            print(f"line: {line}")
            try:
                line_strip = line.split('-')
                hoursBetweenCycles = float(line_strip[0])*60*60
                cycleCount = int(line_strip[1])
            except:
                print("Error with parsing line")
        
            fp.close()
        except:
            print("Error occured in trying to open status file")


        return True
    else:
        return False




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
                     print("Motor on")
                     GPIO.output(4, 1)
                     motorRunning = True
                     mm = False
                     while motorRunning is True: 
                         #val = sw.buttonIn()
                         val=1
                         if val == 1:
                             print("switch pressed")
                             mm = True

                         if val == True and mm == True:
                            print("switch released")
                            motorRunning = False
                            GPIO.output(4, 0)
                            print("motor off")

        else:
            pass

        getStatusIfUpdated()
        getUpatedFile()



except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
    GPIO.cleanup()                 # resets all GPIO ports used by this program


