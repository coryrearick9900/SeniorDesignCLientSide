import serial
import serial.tools.list_ports

#Set the serial stuff up, return a Serial object
def setup():

    #Manual input
    #Set this to /dev/ttyACM0 on the pi
    #COMPort = input("Enter the COM port name you're going to use: ")

    #Autosearch for COM port - "USB Serial Device" or "IFX CDC" on pi
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if (('USB Serial Device' in p.description) or ('IFX CDC' in p.description)):
            COMPort = p.device

    #Initialize the serial port
    serPort = serial.Serial(COMPort, 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)

    return serPort

#Setup the units and bottom threshold
def setUnits(serPort):
    strIn = "US\n"
    #Write to comport
    serPort.write(strIn.encode('ascii')) #Set units to MPH
    print(str(serPort.readline()))

    strIn = "R>3\n" #Requires a newline after input, because Pyserial doesn't have a writeline function
    serPort.write(strIn.encode('ascii')) #Ignore if speed is less than 3 mph - Hardcoded (Can be changed later, though)
    print(str(serPort.readline()))


#Threshold changing function
def changeSpeed():
    speedThresh = float(input("Enter the new threshold, in MPH: "))
    return speedThresh

#Busy waiting loop - Requires a serial port 
def parseSpeed(serPort):
    #User inputted threshold - Hardcoded to 10 by default
    speedThresh = 10.0
    #Speed variable to track speed
    speed = 0.0
    while(True):
        try:
                speed = float(serPort.readline())
                print(f"{speed:.2f}")
        except ValueError:
            pass
        #Interrupt to change the speed threshold
        except KeyboardInterrupt:
            speedThresh = changeSpeed()
            continue
        if(speed > speedThresh or speed < (speedThresh * -1)):
            #Cory should put his camera logic here
            print("ALERT- Movement detected is greater than " + str(format(speedThresh, '.2f')) + " mph")

#test main function
if __name__ == "__main__":
    port = setup()
    setUnits(port)
    print("\nRadar sensor is now recording\n")
    parseSpeed(port)
    
    # check if its speeding here