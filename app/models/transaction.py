from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # income / expense
    category = Column(String, index=True)
    date = Column(Date, nullable=False)
    note = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())