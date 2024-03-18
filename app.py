import asyncio

from rabbitmq.consumer import consumer_loop
from rabbitmq.publicher import publisher_loop


async def main():
    publisher_task = asyncio.create_task(publisher_loop())
    consumer_task = asyncio.create_task(consumer_loop())
    await asyncio.gather(publisher_task, consumer_task)


if __name__ == "__main__":
    asyncio.run(main())
