import sys
import pika
import getpass
import argparse
import os

channel = None


def on_connected(connection):
    """Called when we are fully connected to RabbitMQ"""
    connection.channel(on_open_callback=on_channel_open)
    print("Connected...")


def on_channel_open(new_channel):
    """Called when our channel has opened"""
    global channel
    channel = new_channel
    channel.exchange_declare(exchange='test')
    channel.queue_declare(queue="test", durable=True, exclusive=False,
                          auto_delete=False, callback=on_queue_declared)
    channel.queue_bind(exchange='test', queue='test')
    print("Channel opened...")


def on_queue_declared(frame):
    """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ"""
    channel.basic_consume('test', handle_delivery)
    print("Consuming...")


def handle_delivery(channel, method, header, body):
    """Called when we receive a message from RabbitMQ"""
    print(f"{body}")


def on_close(connection, exception):
    """Called when the connection is closed"""
    connection.ioloop.stop()
    print(f"Closing...")


def get_credentials(username):
    """Retrive password when username is specified"""
    if username:
        try:
            if "AMQP_PWD" in os.environ:
                # Si existe una variable de entorno la tomamos
                password = os.environ["AMQP_PWD"]
            else:
                # De lo contrario la solicitamos al usuario
                password = getpass.getpass(prompt='Password: ', stream=None)
        except getpass.GetPassWarning as e:
            print(f"{e}")
            sys.exit(1)
        else:
            credentials = pika.PlainCredentials(args.user, password)

            return credentials
    else:
        return None


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='Consumer')
    parser.add_argument('-o', '--host', default='localhost')
    parser.add_argument('-p', '--port', default=5672)
    parser.add_argument('-U', '--user')

    args = parser.parse_args()

    credentials = get_credentials(args.user)

    if credentials:
        parameters = pika.ConnectionParameters(
            host=args.host, port=args.port, credentials=credentials)
    else:
        parameters = pika.ConnectionParameters(host=args.host, port=args.port)

    connection = pika.SelectConnection(
        parameters=parameters, on_open_callback=on_connected, on_close_callback=on_close)

    try:
        connection.ioloop.start() 
    except KeyboardInterrupt as e:
        # Close the connection
        connection.close()
        connection.ioloop.start() 
