from pydantic import BaseModel
from datetime import date
from typing import Optional

# 공통 필드
class TransactionBase(BaseModel):
    date: date
    category: str
    description: Optional[str] = None
    amount: float
    transaction_type: str  # "income" or "expense"

    class Config:
        from_attributes = True

# 생성할 때 사용 (id가 없음)
class TransactionCreate(TransactionBase):
    pass

# 조회할 때 사용 (id 포함)
class TransactionResponse(TransactionBase):
    id: int