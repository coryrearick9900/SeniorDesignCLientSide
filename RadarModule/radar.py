"""
import serial
import serial.tools.list_ports
import time

import pika

import json

import datetime

import sys
import os

HOSTNAME = 'localhost'

current_threshhold = 0.0

#Set the serial port up, return a Serial object
def setup():
    
    PORT = '/dev/ttyACM0'

    #Manual input
    #Set this to /dev/ttyACM0 on the pi
    #COMPort = input("Enter the COM port name you're going to use: ")

    #Autosearch for COM port - "USB Serial Device" or "IFX CDC" on pi
    ports = serial.tools.list_ports.comports()
    
    for p in ports:
        print("Ports is ", p)
        if (('USB Serial Device' in p.description) or ('IFX CDC' in p.description)):
            COMPort = p.device
            
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
def changeSpeed(ch, method, props, body):
    global current_threshhold
    
    current_threshhold = body

def gather_threshold(queue_channel):
    
    queue_channel.basic_consume(
        queue='changes',
        auto_ack=True,
        on_message_callback=changeSpeed
    )
    
    if (queue_channel.method.message_count > 0):
        queue_channel.start_consuming()

    
    
current_threshhold = 2

def parseSpeed(serPort, readings, incidents):
    print("Time to parse!!!!")
    #User inputted threshold - Hardcoded to 10 by default
    speedThresh = current_threshhold
    #Speed variable to track speed
    speed = 0.0
    
    try:
        speed = float(serPort.readline())
        
        readings.basic_publish(
            exchange='',
            routing_key='readings',
            body=str(speed)
        )
        
        print("Posted ", speed, " to le queue")
        
        if ((speed > speedThresh) or (speed < (speedThresh * -1))):
            body = '{ "speed": ' + str(speed) + ', "timestamp": ' + str(datetime.datetime.now()) + '}'
            
            body_json = json.loads(body)
            
            incidents.basic_publish(exchange='',
                                routing_key='send_incidents', 
                                body=body_json
                                )
    except ValueError:
        pass

#test main function
if __name__ == "__main__":
    
    print("Waiting for backend server to start...")
    time.sleep(3)
    
    print("Running radar")
    
    rabbit_mq_setup_success = False
    serial_port_setup_success = False
    
    while(not rabbit_mq_setup_success):
        try:
            
            connection = pika.BlockingConnection(pika.ConnectionParameters(HOSTNAME))
            
            readings_channel = connection.channel()
            incidents_channel  = connection.channel()
            changes_channel  = connection.channel()
            
            readings_channel.queue_declare('readings')
            incidents_channel.queue_declare('incidents')
            changes_channel.queue_declare('changes')
            
            rabbit_mq_setup_success = True
            
        except KeyboardInterrupt:
            print("Program terminations detected.\nStopping the radar detection...")
            
            readings_channel = connection.close()
            incidents_channel  = connection.close()
            changes_channel  = connection.close()
            
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
            
            
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ could not be set up properly r")
    
    current_threshhold = 2
    
    while(not serial_port_setup_success):
        try:
            port = setup()
            setUnits(port)
            
            serial_port_setup_success = True
            
        except KeyboardInterrupt:
            print("Program terminations detected.\nStopping the radar detection...")
                
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

        except:
            print("Serial port could not be initialized")
    
    while(rabbit_mq_setup_success and serial_port_setup_success):
        
        try:
        
            #gather_threshold(changes_channel)
            
            parseSpeed(port, readings_channel, incidents_channel)
            
            time.sleep(0.5)
        except KeyboardInterrupt:
            
            print("Stopping radar collection\nPurging Queue")
            
            readings_channel.queue_purge('readings')
            
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        
"""