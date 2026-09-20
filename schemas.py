from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class TransactionType(str, Enum):
    expense = "expense"
    income = "income"

class Transaction(BaseModel):
    transaction_type: TransactionType
    value: float
    description: str
    date: datetime
    category: str

class TransactionOut(Transaction):
    transaction_id: int 