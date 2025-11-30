from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class SubscriptionBase(BaseModel):
    name: str
    amount: float
    cycle: str
    next_due: date
    category: str
    notes: Optional[str] = None

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    cycle: Optional[str] = None
    next_due: Optional[date] = None
    category: Optional[str] = None
    notes: Optional[str] = None

class SubscriptionOut(SubscriptionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
