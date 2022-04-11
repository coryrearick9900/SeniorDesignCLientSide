#!/usr/bin/env python
import pika
import random as rand

def make_number():
    number =  rand.randint(0, 10)
    return number

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='my_queue')

body = "Number is " + str(make_number())

channel.basic_publish(exchange='', routing_key='my_queue', body=body)
print("Sent a message to the queue!")
connection.close()