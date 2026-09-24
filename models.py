from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Enum
)
from database import Base
from schemas import TransactionType

class TransactionDB(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)
    description = Column(String)
    date = Column(DateTime)
    category = Column(String)
    transaction_type = Column(Enum(TransactionType))