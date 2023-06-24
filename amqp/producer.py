import sys
import pika
import time
import random
import getpass
import argparse


def get_credentials(username):
    """Retrive password when username is specified"""
    if username:
        try:
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

    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange='test')

    no = 1

    try:
        while True:
            channel.basic_publish(exchange='test', routing_key='test', body=f'Hello World! {no}')
            no += 1
            time.sleep(random.random() * (71/13))
    except KeyboardInterrupt as e:
        print(f"closing...")
        channel.close()
