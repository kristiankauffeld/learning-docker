from fastapi import FastAPI
from aio_pika import connect_robust, IncomingMessage
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
connection = None
channel = None

async def on_message(message: IncomingMessage):
    async with message.process():
        logging.info("Received a message from RabbitMQ.")
        try:
            body_json = json.loads(message.body.decode('utf-8'))
            logging.info(f"Received audio for stem separation: {body_json}")
        except json.JSONDecodeError:
            logging.error("Received a message that could not be decoded as JSON.")

@app.on_event("startup")
async def startup_event():
    global connection, channel
    logging.info("Starting up...")
    connection = await connect_robust(
        f"amqp://{parsed_url.username}:{parsed_url.password}@{parsed_url.hostname}:{parsed_url.port}/"
    )
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name, durable=True)
    await queue.consume(on_message)

@app.on_event("shutdown")
async def shutdown_event():
    global connection
    logging.info("Shutting down...")
    if connection:
        await connection.close()

@app.get("/")
def index():
    logging.info("Received a GET request on the / endpoint.")
    return {"details": "Hello d"}
