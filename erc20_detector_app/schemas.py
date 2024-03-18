from pydantic import BaseModel, ConfigDict


class ContractDataToAnalyze(BaseModel):
    id: int
    source_code: str

    model_config = ConfigDict(from_attributes=True)


class UpdateContractData(BaseModel):
    status: str
    is_erc_20: bool

    model_config = ConfigDict(from_attributes=True)


class UpdateContractStatus(BaseModel):
    status: str

    model_config = ConfigDict(from_attributes=True)
