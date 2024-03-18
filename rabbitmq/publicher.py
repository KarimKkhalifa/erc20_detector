import asyncio
import json
import logging

from config import settings
from erc20_detector_app import ContractAnalyzeService
from erc20_detector_app.models import ContractStatus
from erc20_detector_app.schemas import UpdateContractStatus
from erc20_detector_app.storages import ContractStorage
from rabbitmq import AsyncRabbitMQ

logging.basicConfig(level=logging.INFO)


async def publisher_loop():
    rabbitmq = AsyncRabbitMQ(settings.rabbitmq_url)
    contract_storage = ContractStorage()
    contract_service = ContractAnalyzeService(contract_storage, rabbitmq)

    while True:
        try:
            contracts, contract_ids = await contract_service.get_contracts(settings.ROWS_LIMIT)
            if contracts:
                message = json.dumps([contract.dict() for contract in contracts])
                await rabbitmq.publish_message(settings.CONTRACTS_QUEUE, message)
                await contract_storage.bulk_update_contract(
                    contract_ids, UpdateContractStatus(status=ContractStatus.WITH_PROCESSING)
                )
            else:
                logging.info("No contracts to publish.")  # Changed print to logging
            await asyncio.sleep(settings.RETRY_INTERVAL)
        except Exception as e:
            logging.error("Publisher Error: %s", e, exc_info=True)  # Log the exception with traceback
            await asyncio.sleep(settings.ERROR_RETRY_INTERVAL)


if __name__ == "__main__":
    asyncio.run(publisher_loop())
