import json
from loguru import logger

import aio_pika


async def get_channel():
    try:
        logger.info("Connecting to RabbitMQ...")
        connection = await aio_pika.connect_robust("amqp://user:user@queue/")
        channel = await connection.channel()
        logger.info("Connected to RabbitMQ and channel created.")
        return channel
    except Exception as e:
        logger.error(f"Error connecting to RabbitMQ: {e}")
        raise


async def send_to_queue(data):
    try:
        message = aio_pika.Message(body=json.dumps(data).encode())
        channel = await get_channel()

        queue = await channel.declare_queue("parcel_queue", durable=True)
        logger.info(f"Queue '{queue.name}' declared.")

        await channel.default_exchange.publish(message, routing_key=queue.name)
        logger.info("Message published to the queue.")

        await channel.close()
        logger.info("Channel closed.")
    except Exception as e:
        logger.error(f"Error sending message to queue: {e}")
        raise
