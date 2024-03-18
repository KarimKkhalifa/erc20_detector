from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base
from erc20_detector_app.models import CompressedText


class ContractStatus(Enum):
    WITH_PROCESSING = "WITH_PROCESSING"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"


class Contract(Base):
    __tablename__ = "Contract"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    contract_address: Mapped[str] = mapped_column(unique=True)
    source_code: Mapped[str] = mapped_column(CompressedText, nullable=False)
    is_erc_20: Mapped[bool] = mapped_column(default=None, nullable=True)
    erc_20_version: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[ContractStatus] = mapped_column(default=ContractStatus.WITH_PROCESSING,
                                                   nullable=False)
