from typing import List
from sqlalchemy import select, update
from erc20_detector_app.models import Contract as ContractModel, ContractStatus
from erc20_detector_app.schemas import ContractDataToAnalyze, UpdateContractData, UpdateContractStatus
from db.db import sessionmanager


class ContractStorage:
    """
    ContractStorage provides functionality to interact with contract data stored in the database.
    It supports fetching contracts for analysis and updating the status of multiple contracts in bulk.
    """
    _table = ContractModel

    @classmethod
    async def fetch_contracts_to_analyze(cls, limit: int) -> List[ContractDataToAnalyze]:
        """
        Fetches a list of contracts that are either in PROCESSING or FAILED status, up to a specified limit.

        Args:
            limit (int): The maximum number of contracts to fetch.

        Returns:
            List[ContractDataToAnalyze]: A list of ContractDataToAnalyze instances representing contracts
            ready for analysis.
        """
        async with sessionmanager.session() as session:
            query = select(cls._table).where(
                cls._table.status.in_([ContractStatus.PROCESSING, ContractStatus.FAILED])
            ).limit(limit)
            result = await session.execute(query)
            contracts = result.scalars().all()

        return [ContractDataToAnalyze.from_orm(contract) for contract in contracts]

    @classmethod
    async def bulk_update_contract(cls, ids: List[int],
                                   update_data: UpdateContractData | UpdateContractStatus) -> None:
        """
        Bulk updates the status and ERC-20 compliance of contracts identified by their IDs.

        Args:
            ids (List[int]): A list of contract IDs to update.
            update_data (UpdateContractData): An instance of UpdateContractData containing the new status
            and ERC-20 compliance flag.

        Returns:
            None
        """
        async with sessionmanager.session() as session:
            await session.execute(
                update(cls._table).where(cls._table.id.in_(ids)).values(
                    **update_data.dict()
                )
            )
            await session.commit()
