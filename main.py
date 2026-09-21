from fastapi import FastAPI, HTTPException
from schemas import (
    Transaction,
    TransactionType,
    TransactionOut
)

app = FastAPI()
transactions_list = []
transaction_id_counter = 0 # if 0 transactions presented, its count is 0. 

@app.get("/")
def get_app():
    return {"message":"hello"}

@app.get("/transactions")
def get_transactions():
    return transactions_list

@app.get("/transactions/summary")
def get_summary_by_categories():
    sum_by_categories = dict()
    for transaction in transactions_list:
        if transaction.transaction_type == TransactionType.income:
            sum_by_categories[transaction.category] = sum_by_categories.get(transaction.category, 0) + transaction.value
        elif transaction.transaction_type == TransactionType.expense:
            sum_by_categories[transaction.category] = sum_by_categories.get(transaction.category, 0) - transaction.value
    return sum_by_categories

@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int):
    for transaction in transactions_list:
        if transaction.transaction_id == transaction_id:
            return transaction
    raise HTTPException(
        status_code=404, 
        detail=f"Transaction with id {transaction_id} not found"
        )

@app.post("/transactions", response_model=TransactionOut)
def add_transaction(transaction: Transaction):
    global transaction_id_counter
    transaction_id_counter += 1
    transaction_out = TransactionOut(**transaction.model_dump(), transaction_id = transaction_id_counter)
    transactions_list.append(transaction_out)
    return transaction_out

@app.put("/transactions/{transaction_id}", response_model=TransactionOut)
def update_transaction(
    transaction_id: int,
    updated_transaction: Transaction
    ):
    for index, transaction in enumerate(transactions_list):
        if transaction.transaction_id == transaction_id:
            transaction_out = TransactionOut(
                **updated_transaction.model_dump(),
                transaction_id = transaction.transaction_id)
            transactions_list[index] = transaction_out
            return transaction_out
    raise HTTPException(
        status_code=404, 
        detail=f"Transaction with id {transaction_id} not found"
        )

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):
    for index, transaction in enumerate(transactions_list):
        if transaction.transaction_id == transaction_id:
            transactions_list.pop(index)
            return {"detail": "Transaction deleted successfully"}
    raise HTTPException(
            status_code=404,
            detail=f"Transaction with id {transaction_id} NOT deleted."
    )