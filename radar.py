#!/usr/bin/env python
from datetime import datetime
from matplotlib.font_manager import json_dump
import pika
import serial
import serial.tools.list_ports as p_list
import json
import datetime

def setup():
    ports = p_list.comports()
    
    for p in ports:
        if (('USB Serial Device' in p.description) or ('IFX CDC' in p.description)):
            COMPort = p.device
    
    serPort = serial.Serial(COMPort, 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
    print("Setup")
    return serPort

def setUnits(serPort):
    strIn = "US\n"
    
    serPort.write(strIn.encode('ascii'))
    print(str(serPort.readline()))
    
    serIn = "R>3\n"
    serPort.write(strIn.encode('ascii'))
    
    print(str(serPort.readling()))
    
def parseSpeed(serPort, channel):
    speedThresh = 2
    
    speed = 0.0
    
    try:
        speed = float(serPort.readline())
    except ValueError:
        print("Error in reading")
        pass
    
    
    if (speed < 0):
        speed *= -1
    
    print(f"Found speed of {speed} mph")
    
    if (speed > speedThresh):
        
        print(f"Time to send {speed}")
        
        current_time = str(datetime.datetime.now())
        
        print(current_time)
        
        data = "{\"speed\":" + str(speed) + ", \"timestamp\": " + current_time + "}"
        
        incident = json.dumps(data)
        
        channel.basic_publish(exchange='', routing_key='radar', body=incident)
        
        print(f"Sent {speed} mph")


if __name__ == "__main__":
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='radar')
    
    port = setup()
    
    while(True):
        try:
            parseSpeed(port, channel)
        except KeyboardInterrupt:
            break
        
    connection.close()