from fastapi import FastAPI
import os
from urllib.parse import urlparse
import pika
import json

app = FastAPI(debug=True)

RABBIT = os.getenv("RABBIT")

if RABBIT is None:
    raise ValueError("RABBIT environment variable is not set")

parsed_url = urlparse(RABBIT)
queue_name = "uploaded"



    # Connect to RabbitMQ
try:
    print(f"Parsed RabbitMQ URL: {parsed_url}")
    print(f"Hostname: {parsed_url.hostname}")
    print(f"Port: {parsed_url.port}")
    print(f"Username: {parsed_url.username}")
    print(f"Password: {parsed_url.password}")
    connection = pika.BlockingConnection( pika.ConnectionParameters( host=parsed_url.hostname, port=parsed_url.port, credentials=pika.PlainCredentials(parsed_url.username, parsed_url.password), ))
except Exception as e:
    print(f"Failed to connect to RabbitMQ: {e}")
    raise





@app.get("/")
def read_root():
    return {"message": "hello hjhj"}


