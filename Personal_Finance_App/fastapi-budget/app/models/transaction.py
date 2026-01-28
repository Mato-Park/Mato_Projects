from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.sql import func
from app.db.base import Base  # 혹은 database.py의 Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=func.now(), nullable=False)
    category = Column(String, index=True, nullable=False)  # 식비, 교통비 등
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)  # "income" or "expense"