#Imagen desde la que partimos
FROM python:3.11

# Instalamos dependencias
RUN pip install pika

# Copiamos los archivos al contenedor
WORKDIR /app
COPY . /app

# Ejecutamos el proceso principal
CMD ["python", "/app/consumer.py"]