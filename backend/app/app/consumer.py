import asyncio
import json
import os
from typing import Any
from loguru import logger

from aio_pika import connect, IncomingMessage, Connection
from loguru import logger
from tortoise import Tortoise
from tortoise.transactions import atomic

from models.tortoise import Parcel
from utils import calculate_delivery_cost


def get_db_config() -> dict[str, Any]:
    # Retrieve database configuration settings
    return {
        "connections": {"default": os.getenv("DATABASE_URL")},
        "apps": {
            "models": {
                "models": ["models.tortoise"],
                "default_connection": "default",
            }
        },
    }


async def init_db() -> None:
    """
    Initialize the database connection using the Tortoise ORM.

    The database configuration is taken from environment variables. Ensure these
    are set correctly in the environment.
    """
    config = get_db_config()
    await Tortoise.init(config=config)


@atomic()
async def save_parcel_async(data: dict, delivery_cost_cents: int) -> str:
    """
    Asynchronously save parcel data to the database.

    Args:
    data (dict): A dictionary containing parcel data.
    delivery_cost_cents (int): The calculated delivery cost in cents.

    Returns:
    str: The unique ID of the created parcel record.
    """
    parcel = await Parcel.create(
        name=data["name"],
        weight=data["weight"],
        content_value_cents=data["content_value_cents"],
        delivery_cost_cents=delivery_cost_cents,
        parcel_type_id=data.get("parcel_type_id"),
        session_id=data.get("session_id"),
    )
    parcel_id = str(parcel.id)
    logger.info(f"Parcel saved with ID: {parcel_id}")

    return parcel.id


async def on_message(message: IncomingMessage) -> None:
    """
    Handles incoming RabbitMQ messages by processing and saving parcel data.

    Args:
        message (IncomingMessage): Message received from RabbitMQ.

    Processes the message, calculates delivery cost, saves to database, and logs any errors.
    """
    logger.info("Received message from RabbitMQ.")
    try:
        async with message.process():
            data = json.loads(message.body.decode())
            logger.info(f"Processing parcel data: {data}")
            delivery_cost = calculate_delivery_cost(
                data["weight"], data["content_value_cents"]
            )
            logger.info(f"Calculated delivery cost: {delivery_cost} cents")
            await save_parcel_async(data, delivery_cost)
            logger.info("Parcel processed successfully.")
    except Exception as e:
        logger.error(f"Error processing message: {e}")


async def main() -> Connection:
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized.")

    logger.info("Connecting to RabbitMQ...")
    conn = await connect("amqp://user:user@queue/")
    logger.info("Connected to RabbitMQ.")

    channel = await conn.channel()
    queue = await channel.declare_queue("parcel_queue", durable=True)
    await queue.consume(on_message)
    logger.info("Consumer set up completed.")

    return conn


if __name__ == "__main__":
    # Running the main function in an event loop
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main())
    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
        loop.run_until_complete(Tortoise.close_connections())
