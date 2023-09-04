from fastapi import FastAPI
import pika
import os
from urllib.parse import urlparse
import threading
import json
import logging

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)


app = FastAPI(debug=True)

# RabbitMQ server connection parameters
RABBIT = os.getenv("RABBIT")

parsed_url = urlparse(RABBIT)
queue_name = "uploaded"

try:
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=parsed_url.hostname,
            port=parsed_url.port,
            credentials=pika.PlainCredentials(parsed_url.username, parsed_url.password),
        )
    )
except Exception as e:
    print(f"Could not connect to RabbitMQ: {e}")
    exit(1)

channel = connection.channel()

channel.queue_declare(
    queue=queue_name, durable=True
)  

def consume_uploaded_message(ch, method, properties, body):
    logging.info("Received a message from RabbitMQ.")
    try:
        message = json.loads(body.decode('utf-8'))
        logging.info(f"Received audio for stem separation: {message}")
    except json.JSONDecodeError:
        logging.error("Received a message that could not be decoded as JSON.")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue=queue_name, on_message_callback=consume_uploaded_message, auto_ack=False
)


def start_rabbitmq_consumer():
    try:
        logging.info("Starting to consume messages from RabbitMQ.")
        channel.start_consuming()
    except Exception as e:
        logging.error(f"Error in RabbitMQ consumer: {e}")


rabbitmq_thread = threading.Thread(target=start_rabbitmq_consumer)
rabbitmq_thread.start()


@app.get("/")
def index():
    logging.info("Received a GET request on the / endpoint.")
    return {"details": "Hello"}

