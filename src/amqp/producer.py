import sys
import pika
import time
import random
import getpass
import argparse
import os


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

    print(f"Conectando al servidor {args.host}")
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange='test')

    no = 1

    try:
        while True:
            channel.basic_publish(exchange='test', routing_key='test', body=f'Hello World! {no}')
            no += 1
            print(f"Enviando el mensaje: {no}")
            time.sleep(2.0) # Cambie el envio a intervalos regulares.
    except KeyboardInterrupt as e:
        print(f"closing...")
        channel.close()
