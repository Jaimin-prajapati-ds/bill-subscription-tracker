from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date, timedelta
from backend.database import get_db, init_db, engine
from backend.models import Subscription
from backend.schemas import SubscriptionCreate, SubscriptionUpdate, SubscriptionOut
import os

app = FastAPI(
    title="Bill Subscription Tracker",
    description="Track recurring bills and subscriptions with AI insights",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Bill Subscription Tracker API", "version": "1.0.0"}

@app.post("/subscriptions", response_model=SubscriptionOut)
def create_subscription(sub: SubscriptionCreate, db: Session = Depends(get_db)):
    db_sub = Subscription(**sub.dict())
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

@app.get("/subscriptions", response_model=list[SubscriptionOut])
def list_subscriptions(db: Session = Depends(get_db)):
    subs = db.query(Subscription).order_by(Subscription.next_due).all()
    return subs

@app.get("/subscriptions/{sub_id}", response_model=SubscriptionOut)
def get_subscription(sub_id: int, db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return sub

@app.put("/subscriptions/{sub_id}", response_model=SubscriptionOut)
def update_subscription(sub_id: int, update: SubscriptionUpdate, db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    for key, val in update.dict(exclude_unset=True).items():
        setattr(sub, key, val)
    db.commit()
    db.refresh(sub)
    return sub

@app.delete("/subscriptions/{sub_id}")
def delete_subscription(sub_id: int, db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    db.delete(sub)
    db.commit()
    return {"message": "Subscription deleted"}

@app.get("/subscriptions/due/today")
def get_due_today(db: Session = Depends(get_db)):
    today = date.today()
    subs = db.query(Subscription).filter(Subscription.next_due == today).all()
    return {"count": len(subs), "subscriptions": subs}

@app.get("/subscriptions/due/soon")
def get_due_soon(days: int = 7, db: Session = Depends(get_db)):
    today = date.today()
    future = today + timedelta(days=days)
    subs = db.query(Subscription).filter(
        and_(Subscription.next_due > today, Subscription.next_due <= future)
    ).order_by(Subscription.next_due).all()
    return {"count": len(subs), "subscriptions": subs}

@app.get("/subscriptions/summary/monthly")
def get_monthly_summary(db: Session = Depends(get_db)):
    subs = db.query(Subscription).all()
    summary = {}
    for sub in subs:
        monthly_cost = sub.amount if sub.cycle == "monthly" else sub.amount / 12 if sub.cycle == "annual" else 0
        if sub.category not in summary:
            summary[sub.category] = 0
        summary[sub.category] += monthly_cost
    total = sum(summary.values())
    return {"by_category": summary, "total_monthly": total}

@app.get("/insights/{sub_id}")
def get_ai_insight(sub_id: int, db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    category_subs = db.query(Subscription).filter(Subscription.category == sub.category).all()
    category_total = sum(s.amount if s.cycle == "monthly" else s.amount/12 for s in category_subs)
    insight = f"You spend {category_total:.2f} on {sub.category}. {sub.name} costs {sub.amount}/month."
    return {"subscription_id": sub_id, "insight": insight}
