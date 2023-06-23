import os
import sys
import time
import pika



def connect(host='localhost'):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost', port=5672, credentials=pika.PlainCredentials('user', '1234')))
    channel = connection.channel()

    return channel


if __name__ == "__main__":

    channel = connect()

    channel.exchange_declare(exchange='queue-001', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='queue-001', queue=queue_name)

    print(" [*] Waiting for messages...")

    def callback(ch, method, properties, body):
        print(f" [x] {body}")

    
    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True
    )

    try:
        channel.start_consuming()
    except KeyboardInterrupt as e:
        print(f"Error: {e}, closing...")
        channel.close()
        sys.exit(0)
