import json
import logging
from typing import Optional, Tuple, List, Dict, Any, Union

from erc20_detector_app.constants import ALLOWED_TOKENS, REGEX_PATTERN
from erc20_detector_app.models import ContractStatus
from erc20_detector_app.schemas import ContractDataToAnalyze, UpdateContractData
from erc20_detector_app.storages import ContractStorage
from rabbitmq import AsyncRabbitMQ


class ContractAnalyzeService:
    """
    Service for analyzing contract source code to determine compliance with ERC20 standards.

    Attributes:
        _contract_storage (ContractStorage): Storage system for contracts.
        _rabbitmq (AsyncRabbitMQ): RabbitMQ message broker client.
    """

    def __init__(self, contract_storage: ContractStorage, rabbitmq: AsyncRabbitMQ) -> None:
        """
        Initialize the ContractAnalyzeService with contract storage and RabbitMQ client.

        Args:
            contract_storage (ContractStorage): The storage system for contracts.
            rabbitmq (AsyncRabbitMQ): The RabbitMQ message broker client.
        """
        self._contract_storage = contract_storage
        self._rabbitmq = rabbitmq

    async def get_contracts(self, limit: int) -> Optional[Tuple[List[ContractDataToAnalyze], List[int]]]:
        """
        Fetches contracts up to a specified limit and extracts their IDs.

        Args:
            limit (int): The maximum number of contracts to fetch.

        Returns:
            Optional[Tuple[List[ContractDataToAnalyze], List[int]]]: A tuple containing a list of contracts
            and their IDs, or None if no contracts are found.
        """
        contracts = await self._contract_storage.fetch_contracts_to_analyze(limit)
        contract_ids = [contract.id for contract in contracts]
        return contracts, contract_ids

    async def receive_contracts(self, message: Any) -> None:
        """
        Processes received contract messages by decoding and analyzing them.

        Args:
            message: The message received from the RabbitMQ queue.

        Returns:
            None
        """
        try:
            contracts_data = json.loads(message.body.decode('utf-8'))
            await self.analyze_contracts(contracts_data)
            await message.ack()
        except json.JSONDecodeError as e:
            logging.error(f"JSON decoding error handling message: {e}")
        except Exception as e:
            logging.error(f"Error handling message: {e}")

    async def analyze_contracts(self, contracts_data: List[Dict[str, Any]]) -> None:
        """
        Analyzes contracts to determine if they conform to ERC20 standards based on their source code.

        Args:
            contracts_data (List[Dict[str, Any]]): List of contracts data.

        Returns:
            None
        """
        logging.info('Analyzing contracts')
        erc20_contracts, non_erc20_contracts = self.classify_contracts(contracts_data)

        if erc20_contracts:
            logging.info(f"Updating {len(erc20_contracts)} contracts as ERC20.")
            await self._contract_storage.bulk_update_contract(
                erc20_contracts, UpdateContractData(status=ContractStatus.PROCESSED, is_erc_20=True)
            )

        if non_erc20_contracts:
            logging.info(f"Updating {len(non_erc20_contracts)} contracts as non-ERC20.")
            await self._contract_storage.bulk_update_contract(
                non_erc20_contracts, UpdateContractData(status=ContractStatus.PROCESSED, is_erc_20=False)
            )

    def find_allowed_imports(self, source_code: str) -> List[str]:
        """
        Filters out commented lines and searches for allowed import lines in the given source code.

        Args:
            source_code (str): The source code of a contract.

        Returns:
            List[str]: Allowed import statements found in the source code.
        """
        lines = source_code.split('\n')
        non_comment_lines = [line for line in lines if not line.strip().startswith("//")]
        allowed_imports = [line for line in non_comment_lines if REGEX_PATTERN.search(line)]
        return allowed_imports

    def classify_contracts(self, contracts_data: List[Dict[str, Any]]) -> Tuple[List[int], List[int]]:
        """
        Classifies contracts into ERC20 and non-ERC20 based on their source code.

        Args:
            contracts_data (List[Dict[str, Any]]): List of contracts data.

        Returns:
            Tuple[List[int], List[int]]: Two lists containing the IDs of ERC20 and non-ERC20 contracts respectively.
        """
        erc20_contracts = []
        non_erc20_contracts = []

        for contract in contracts_data:
            # Extract the source code from the contract data
            source_code = contract['source_code']

            # Use the function to find allowed import lines in the contract's source code
            matches = self.find_allowed_imports(source_code)

            # Check if any of the found imports match the allowed tokens
            if matches:
                erc20_contracts.append(contract['id'])
            else:
                non_erc20_contracts.append(contract['id'])

        return erc20_contracts, non_erc20_contracts
