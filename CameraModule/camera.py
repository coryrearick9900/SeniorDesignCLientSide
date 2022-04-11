from platform import python_branch
import pika

import cv2
import numpy

import time
import json
from base64 import b64encode

import sys
from sys import exit
import os

hostname = 'localhost'

incidents_queue = 'incidents'
tickets_queue = 'tickets'

ENCODING = 'utf-8'

def write_to_tickets_queue(ticket):
    tickets_channel.basic_publish(ticket)

def take_image(ch, method, props, body):
    # take a frame from the camera
    img = cv2.read("taken_image.png", cv2.IMREAD_COLOR)
    
    cv2.imshow("Taken Image", img)
    
    with open(img, 'rb') as open_img:
        byte_content = open_img.read()
    
    base64_bytes = b64encode(byte_content)
    
    base64_string = base64_bytes.decode(ENCODING)
    
    # make JSON
    incident_string = '{"speed": ' + body + ', "image":' + base64_string + '}'
    
    incident_json = json.dumps(incident_string)
    
    write_to_tickets_queue(incident_json)
    
    time.sleep(0.5)
    
    cv2.destroyAllWindows()
    
    

if __name__ == "__main__":
    
    rabbit_mq_setup_success = False
    
    print("Camera started")
    
    while(not rabbit_mq_setup_success):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(hostname))

            incidents_channel = connection.channel()
            tickets_channel = connection.channel()
            
                
            rabbit_mq_setup_success = True
            
            incidents_channel.queue_declare(queue=incidents_queue)
            tickets_channel.queue_declare(queue=tickets_queue)
            
        
            incidents_channel.basic_consume(queue=incidents_queue,
                            auto_ack=True,
                            on_message_callback=take_image
                            )
            
            
            incidents_channel.start_consuming()
            
        except KeyboardInterrupt:
            incidents_channel.stop_consuming()
            print("Stopping the camera module")
            
            tickets_channel.close()
            incidents_channel.close()

            
            
                
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ could not be set up properly c")

    