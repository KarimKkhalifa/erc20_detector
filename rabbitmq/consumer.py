import asyncio
import json
import logging

from config import settings
from erc20_detector_app import ContractAnalyzeService
from erc20_detector_app.storages import ContractStorage
from rabbitmq import AsyncRabbitMQ

logging.basicConfig(level=logging.INFO)

rabbitmq = AsyncRabbitMQ(settings.rabbitmq_url)
contract_storage = ContractStorage()
contract_service = ContractAnalyzeService(contract_storage, rabbitmq)


async def consume_message(message):
    try:
        contracts_data = json.loads(message.body.decode('utf-8'))
        await contract_service.analyze_contracts(contracts_data)
        await message.ack()
    except Exception as e:
        logging.error(f"Error handling message: {e}")


async def consumer_loop():
    while True:
        try:
            await rabbitmq.consume_messages(settings.CONTRACTS_QUEUE, consume_message)
        except Exception as e:
            logging.error(f"Consumer Error: {e}")
            await asyncio.sleep(settings.RETRY_INTERVAL)


if __name__ == "__main__":
    asyncio.run(consumer_loop())
