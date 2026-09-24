from fastapi import (
    FastAPI,
    HTTPException
)
from sqlalchemy import select, func
from schemas import (
    Transaction,
    TransactionType,
    TransactionOut
)
from database import SessionLocal
from models import TransactionDB

app = FastAPI()

@app.get("/")
def get_app():
    return {"message":"hello"}

@app.get("/transactions", response_model=list[TransactionOut])
def get_transactions():
    with SessionLocal() as session:
        transactions = session.execute(
            select(TransactionDB)
            .order_by(TransactionDB.id)
            ).scalars().all()
        return transactions

@app.get("/transactions/summary")
def get_summary_by_categories():
    with SessionLocal() as session:
        summary = session.execute(
            select(TransactionDB.category,
            func.sum(TransactionDB.value)
            ).group_by(TransactionDB.category)
        ).all()
    return summary

@app.get("/transactions/{id}", response_model=TransactionOut)
def get_transaction(id: int):
    with SessionLocal() as session:
        transaction = session.execute(
            select(TransactionDB)
            .where(TransactionDB.id == id)
            ).scalars().one_or_none()
        if transaction is None:
            raise HTTPException(
                status_code=404,
                detail=f"Transaction with id {id} not found"
                )
        return transaction

@app.post("/transactions", response_model=TransactionOut)
def add_transaction(transaction: Transaction):
    transaction_db = TransactionDB(**transaction.model_dump())
    with SessionLocal() as session:
        session.add(transaction_db)
        session.commit()
        session.refresh(transaction_db)
        return transaction_db

@app.put("/transactions/{id}", response_model=TransactionOut)
def update_transaction(
    id: int,
    updated_transaction: Transaction
    ):
    with SessionLocal() as session:
        transaction = session.execute(
        select(TransactionDB)
        .where(TransactionDB.id == id)
        ).scalars().one_or_none()
        if transaction is None:
            raise HTTPException(
                status_code=404,
                detail=f"Transaction with id {id} not found"
                )
        upd_tr_dict = updated_transaction.model_dump()
        for key, value in upd_tr_dict.items():
            setattr(transaction, key, value)
        session.commit()
        session.refresh(transaction)
        return transaction

@app.delete("/transactions/{id}")
def delete_transaction(id: int):
    with SessionLocal() as session:
        transaction = session.execute(
            select(TransactionDB).where(TransactionDB.id == id)
        ).scalars().one_or_none()
        if transaction is None:
            raise HTTPException(
                status_code=404,
                detail=f"Transaction with id {id} not found"
                )
        session.delete(transaction)
        session.commit()
        return {
            "detail": f"Transaction with id {id} deleted successfully"
            }