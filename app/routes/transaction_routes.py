from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction_schema import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse
)
from app.dependencies.roles import require_role

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=TransactionResponse)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    user = Depends(require_role(["admin"]))
):
    transaction = Transaction(**data.dict())

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction

@router.get("/", response_model=list[TransactionResponse])
def get_transactions(
    type: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = Query(10, le=100),
    offset: int = 0,
    db: Session = Depends(get_db),
    user = Depends(require_role(["admin", "analyst"]))
):
    query = db.query(Transaction)

    if type:
        query = query.filter(Transaction.type == type)

    if category:
        query = query.filter(Transaction.category == category)

    if start_date:
        query = query.filter(Transaction.date >= start_date)

    if end_date:
        query = query.filter(Transaction.date <= end_date)

    transactions = query.offset(offset).limit(limit).all()

    return transactions

@router.get("/{id}", response_model=TransactionResponse)
def get_transaction(
    id: int,
    db: Session = Depends(get_db),
    user = Depends(require_role(["admin", "analyst"]))
):
    transaction = db.query(Transaction).filter(Transaction.id == id).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction

@router.put("/{id}", response_model=TransactionResponse)
def update_transaction(
    id: int,
    data: TransactionUpdate,
    db: Session = Depends(get_db),
    user = Depends(require_role(["admin"]))
):
    transaction = db.query(Transaction).filter(Transaction.id == id).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(transaction, key, value)

    db.commit()
    db.refresh(transaction)

    return transaction

@router.delete("/{id}")
def delete_transaction(
    id: int,
    db: Session = Depends(get_db),
    user = Depends(require_role(["admin"]))
):
    transaction = db.query(Transaction).filter(Transaction.id == id).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction)
    db.commit()

    return {"message": "Transaction deleted"}