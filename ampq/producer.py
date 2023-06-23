import os
import sys
import time
import pika
import uuid


def connect(host='localhost'):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost', port=5672, credentials=pika.PlainCredentials('user', '1234')))
    channel = connection.channel()

    return channel


if __name__ == "__main__":

    channel = connect()

    channel.exchange_declare(exchange='queue-001', exchange_type='fanout')

    body = "Hello, World"

    try:
        while True:
            channel.basic_publish(
                exchange='queue-001', routing_key=str(uuid.uuid4()), body=body)
            time.sleep(2.5)
    except KeyboardInterrupt as e:
        print(f"Error: {e}, closing...")
        channel.close()
        sys.exit(0)
