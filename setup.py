import os

from setuptools import setup


setup(
    name="ampq",
    version="0.1",
    author="Juan Manuel Carballo",
    author_email="jm.carb@gmail.com",
    install_requires = [
        'pika',
        'argparse'
    ]
)