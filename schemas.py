from pydantic import (
    BaseModel,
    ConfigDict,
    NonNegativeFloat,
)
from datetime import datetime
from enum import Enum

class TransactionType(str, Enum):
    expense = "expense"
    income = "income"

class Transaction(BaseModel):
    transaction_type: TransactionType
    value: NonNegativeFloat
    description: str
    date: datetime
    category: str

class TransactionOut(Transaction):
    model_config = ConfigDict(from_attributes=True)
    id: int