import pika, sys, os

host = 'localhost'
queue = 'radar'

def on_message(ch, method, props, body):
    message = body.decode('UTF-8')
    print(f"I got message {message}.")


if __name__ == "__main__":
    connection_params = pika.ConnectionParameters(host=host)
    connection = pika.BlockingConnection(connection_params)
        
    channel = connection.channel()

    channel.queue_declare(queue=queue)

    channel.basic_consume(queue=queue, on_message_callback=on_message, auto_ack=True)

    print(f"Subscribed to {queue}, waiting for messages")

    channel.start_consuming()