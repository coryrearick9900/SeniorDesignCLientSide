from asyncio.windows_events import NULL
from importlib.resources import Resource
from multiprocessing.sharedctypes import Value
from telnetlib import STATUS
from aiohttp import request
from cv2 import cuda_TargetArchs
from django.shortcuts import render
from itsdangerous import Serializer
from rest_framework import generics, status
from .models import DataPoint, RadarReading, SpeedThreshhold
from .serializers import DataPointSeralizer, RadarSensorSerializer, SpeedThreshholdSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, QueryDict
import json
from datetime import datetime

import serial
import serial.tools.list_ports

import cv2

import pika

import base64

current_reading = ""


def set_current_speed(ch, method, props, body):
        
        payload = '{ "speed": ' + str(body) + ' }'
        
        print("Payload: -----------", payload)
        
        global current_reading
        current_reading = json.dumps(payload)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
incidents_channel = connection.channel()
tickets_channel = connection.channel()
    
incidents_channel.queue_declare('incidents')
tickets_channel.queue_declare('tickets')

class ChangeSpeedThreshhold(APIView):
    
    
    def post(self, request, format=None):
        
        print("-------------------\n-------")
        
        newSpeed = int(request.query_params["newSpeed"])
        print("oi set the speed to ", newSpeed)
        
        serializer = SpeedThreshholdSerializer(data=request.query_params)
        
        print("request is ", request)
        
        if serializer.is_valid():
            print("New speed is ", type(newSpeed), ": ", newSpeed)
            print("psssst 10 more than ", newSpeed, " is ", newSpeed + 10)
            
            queryset = SpeedThreshhold.objects.all()
            
            if queryset.exists():
                print("exists")
                changespeed = queryset[0]
                changespeed.newSpeed = newSpeed
                changespeed.save(update_fields=['newSpeed'])
            else:
                print("no exists")
                changespeed = SpeedThreshhold(newSpeed=newSpeed)
                changespeed.save()
        
        return Response("New Speed is " + str(changespeed.newSpeed), status=status.HTTP_201_CREATED)
            
            

class DataPointView(generics.ListAPIView):
    queryset = DataPoint.objects.all()
    serializer_class = DataPointSeralizer

class RadarReadingView(generics.ListAPIView):
    queryset = RadarReading.objects.all()
    serializer_class = RadarSensorSerializer


host = 'localhost'
queue = 'radar'
readings_queue = 'readings'


class GetDataPoint(generics.ListAPIView):
    
    def set_current_speed(self, ch, method, props, body):
        payload = body['speed']
        
        self.current_speed = payload
        self.current_timestamp = body['timestamp']
    
    current_speed = 0.0
    current_timestamp = ""
    
    serializer_class = DataPointSeralizer
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        
    channel = connection.channel()

    channel.queue_declare(queue=queue)
    
    def get(self, request, format=None):
        
        print("#####################################")
        
        self.channel.basic_consume(queue=queue, on_message_callback=self.set_current_speed, auto_ack=True)
        self.channel.close()
        
        speed = self.current_speed
        
        #speed = 69
        
        print("Speed is ", speed)
        datapoint = {
            "speed": 69,
            "timestamp": "thing"
        }
        
        jsonObject = json.dumps(datapoint)
        
        return HttpResponse(jsonObject, content_type="application/json" ,status=status.HTTP_200_OK)

class Radar:
    
    def setup(self):
        
        self.ports = serial.tools.list_ports.comports()
            
        for p in self.ports:
            #print("P is ", p)
            if (('USB Serial Device' in p.description) or ('IFX CDC' in p.description)):
                COMPort = p.device
                
        serPort = serial.Serial(COMPort, 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
        return serPort


    def setUnits(self, serPort):
        settingAdjustments = ["US\n", "R>0", "Z-"]
        # reports US units ----┘       |      |
        # disables detection limit ----┘      |
        # disables sensor hibernation --------┘
        
        for s in settingAdjustments:
            serPort.write(s.encode('ascii'))
        
    def readSpeed(self, serPort):
        
        try:
            speed = float(serPort.readline())
                
            if (speed != NULL):
                return speed
            else:
                return 0
        except ValueError:
            return 0
            

class Camera():
    def take_image(self):
        camera = cv2.VideoCapture(0)
        
        ret_val, frame = camera.read()
        
        img_string = cv2.imencode('.png', frame)[1].tostring()
        
        # return frame, and the encoded image
        b64_string = ""
        
        with open(frame, "rb"):
            b64_string = base64.b64encode(frame.read())
            
        
        return frame, b64_string
        
        
        #print("Frame is ", img_string)

print("make port?")
radar = Radar()
port = radar.setup()
radar.setUnits(port)

class GetSpeedThreshhold(generics.ListAPIView):
    def get(self, request, format=None):
        serializer = SpeedThreshholdSerializer(data=request.query_params)
        speedThresh = 0
        
        if serializer.is_valid():
            queryset = SpeedThreshhold.objects.all()
            
            for i in queryset:
                print("each: ", i)
                print("i.newSpeed = ", i.newSpeed)
                speedThresh = i.newSpeed
            
            json_speed = '{ "newSpeed": ' + str(speedThresh) + '}'
            
            json_obj = json.loads(json_speed)
        
        
            return Response(json_obj, status=status.HTTP_200_OK)
        else:
            return Response("Could not collect current speed threashold", status=status.HTTP_204_NO_CONTENT)

class GetLastSpeed(generics.ListAPIView):
    
    def get(self, request, format=None):
        
        last_speed = -999
        
        serializer = SpeedThreshholdSerializer(data=request.query_params)
        speedThresh = 0
        
        if serializer.is_valid():
            queryset = SpeedThreshhold.objects.all()
            
            for i in queryset:
                print("each: ", i)
                print("i.newSpeed = ", i.newSpeed)
                speedThresh = i.newSpeed
        
        try:
            if(port.isOpen):
                
                print("radar is open")
                
                # ------ TIMEOUT AFTER 0.3 SECONDS --------
                last_speed = radar.readSpeed(port)
                print("got ", last_speed)
                # -----------------------------------------
                
                if (speedThresh != 0):
                    if ((last_speed > speedThresh) or (last_speed < (speedThresh * -1))):
                        # add an incident to the incidents queue
                        
                        camera = Camera()
                        image, encoded_image = camera.take_image()
                        
                        timestamp = datetime.now()
                        
                        new_incident_str = '{ "speed": ' + str(last_speed) + ', "timestamp": ' + str(timestamp) + ', "image": ' + encoded_image + '}'
                        short_incident = '{ "speed": ' + str(last_speed) + ', "timestamp": ' + str(timestamp) + ', "image": ' + encoded_image[:20] + '}'
                        
                        print(short_incident)
                        
                        new_incident_json = json.loads(new_incident_str)
                        
                        # Add the new incident to the queue
                        # Then it must go to the actual database
                        
                        
                        
                    
                    
                    
            else:
                print("radar is closed")
                return HttpResponse("Could not read from the sensor", content_type="application/json", status=status.HTTP_503_SERVICE_UNAVAILABLE)
                    
            
            
            return HttpResponse(last_speed, content_type="application/json", status=status.HTTP_200_OK)
        except serial.serialutil.SerialException:
            return HttpResponse("Could not read from the sensor", content_type="application/json", status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except ValueError:
            return HttpResponse(0, content_type="application/json", status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
        
        
        
        
    #   return HttpResponse(jsonObject, content_type="application/json" ,status=status.HTTP_200_OK)
