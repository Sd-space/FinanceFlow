from pydantic import BaseModel, validator
from datetime import date
from typing import Optional
from app.models.enums import TransactionType

class TransactionCreate(BaseModel):
    amount: float
    type: TransactionType
    category: str
    date: date
    note: Optional[str] = None

    @validator("amount")
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v

    # @validator("type")
    # def valid_type(cls, v):
    #     if v not in ["income", "expense"]:
    #         raise ValueError("Type must be 'income' or 'expense'")
    #     return v


class TransactionUpdate(BaseModel):
    amount: Optional[float]
    type: Optional[str]
    category: Optional[str]
    date: Optional[date]
    note: Optional[str]


class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: date
    note: Optional[str]

    class Config:
        orm_mode = True