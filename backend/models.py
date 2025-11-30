from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from datetime import datetime
from backend.database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    cycle = Column(String(50), nullable=False)  # monthly, annual, one-time
    next_due = Column(Date, nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
