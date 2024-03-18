import aio_pika
from typing import Any, Optional
import asyncio
import logging


class AsyncRabbitMQ:
    """
    An asynchronous context manager and client for RabbitMQ operations using aio_pika, implemented as a Singleton.

    This class provides simplified methods to publish and consume messages from RabbitMQ queues.
    Only one instance of this class is allowed to exist in the application context.
    """

    _instance: Optional['AsyncRabbitMQ'] = None

    def __new__(cls, url: str) -> 'AsyncRabbitMQ':
        if cls._instance is None:
            cls._instance = super(AsyncRabbitMQ, cls).__new__(cls)
            cls._instance.url = url
            cls._instance.connection = None
            cls._instance.channel = None
        return cls._instance

    async def connect(self, retry_count=0, max_retries=5):
        if retry_count > max_retries:
            logging.error("Max retry attempts reached. Failed to connect to RabbitMQ.")
            return
        try:
            self.connection = await aio_pika.connect_robust(self.url)
            self.channel = await self.connection.channel()
        except Exception as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}")
            self.connection = None
            self.channel = None
            await asyncio.sleep(2 ** retry_count)  # Exponential backoff
            await self.connect(retry_count + 1, max_retries)

    async def __aenter__(self) -> 'AsyncRabbitMQ':
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Optional[type], exc_val: Optional[Exception],
                        exc_tb: Optional[Any]) -> None:
        if self.channel is not None:
            try:
                await self.channel.close()
            except Exception as e:
                logging.error(f"Failed to close RabbitMQ channel: {e}")
        if self.connection is not None:
            try:
                await self.connection.close()
            except Exception as e:
                logging.error(f"Failed to close RabbitMQ connection: {e}")
        self.connection = None
        self.channel = None

    async def publish_message(self, queue_name: str, message: str) -> None:
        try:
            if not self.channel:
                await self.connect()
            await self.channel.default_exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=queue_name,
            )
        except Exception as e:
            logging.error(f"Failed to publish message: {e}")

    async def consume_messages(self, queue_name: str, callback: callable) -> None:
        try:
            if not self.channel:
                await self.connect()
            queue = await self.channel.declare_queue(queue_name)
            await queue.consume(callback)
        except Exception as e:
            logging.error(f"Failed to consume messages: {e}")
