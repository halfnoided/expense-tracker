from fastapi import FastAPI, HTTPException
from schemas import Transaction, TransactionType, TransactionOut

app = FastAPI()
transactions_list = []
transaction_id_counter = 0 # if 0 transactions presented, its count is 0. 

@app.get("/")
def get_app():
    return {"message":"hey"}

@app.get("/transactions")
def get_transactions():
    return transactions_list

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
