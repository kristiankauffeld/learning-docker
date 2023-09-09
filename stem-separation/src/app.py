from fastapi import FastAPI, Depends
from aio_pika import connect_robust, IncomingMessage
import os
from urllib.parse import urlparse
import json
import logging

# Import database components
from .database import engine, SessionLocal
from . import crud, models, schemas

logging.basicConfig(level=logging.INFO)

# Initialize the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

RABBIT = os.getenv("RABBIT")
DB_URL = os.getenv('DB_URL')

logging.info(f"Database URL: {DB_URL}")

 # RabbitMQ setup
parsed_url = urlparse(RABBIT)
queue_name = "uploaded"
connection = None
channel = None

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def on_message(message: IncomingMessage):
    async with message.process():
        logging.info("Received a message from RabbitMQ.")
        db = SessionLocal()  # Explicitly create a session
        try:
            body_json = json.loads(message.body.decode('utf-8'))
            logging.info(f"Received audio for stem separation: {body_json}")

            received_file_path = body_json.get('filePath')
            if received_file_path:
                file_schema = schemas.CreateUploadedFileSchema(file_path=received_file_path)
                new_record = crud.create_uploaded_file(db=db, uploaded_file=file_schema)
                if new_record.id:
                    logging.info(f"New record added with ID {new_record.id}")

            db.commit()  # Commit the transaction

        except json.JSONDecodeError:
            logging.error("Received a message that could not be decoded as JSON.")
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            db.rollback()  # Rollback the transaction in case of an error
        finally:
            db.close()  # Close the session

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
    return {"details": "Hello"}
