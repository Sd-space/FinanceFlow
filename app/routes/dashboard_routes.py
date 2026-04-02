from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.database import get_db
from app.models.transaction import Transaction
from app.dependencies.roles import require_role

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    user = Depends(require_role(["admin", "analyst", "viewer"]))
):
    total_income = db.query(func.sum(Transaction.amount))\
        .filter(Transaction.type == "income").scalar() or 0

    total_expense = db.query(func.sum(Transaction.amount))\
        .filter(Transaction.type == "expense").scalar() or 0

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense
    }

@router.get("/category-breakdown")
def category_breakdown(
    db: Session = Depends(get_db),
    user = Depends(require_role(["admin", "analyst"]))
):
    results = db.query(
        Transaction.category,
        func.sum(Transaction.amount)
    ).group_by(Transaction.category).all()

    return {category: total for category, total in results}

@router.get("/monthly-trends")
def monthly_trends(
    db: Session = Depends(get_db),
    user = Depends(require_role(["admin", "analyst"]))
):
    results = db.query(
        extract("month", Transaction.date).label("month"),
        Transaction.type,
        func.sum(Transaction.amount)
    ).group_by("month", Transaction.type).all()

    trends = {}

    for month, t_type, total in results:
        month = int(month)
        if month not in trends:
            trends[month] = {"income": 0, "expense": 0}
        trends[month][t_type] = total

    return trends

@router.get("/recent")
def recent_transactions(
    db: Session = Depends(get_db),
    user = Depends(require_role(["admin", "analyst", "viewer"]))
):
    transactions = db.query(Transaction)\
        .order_by(Transaction.date.desc())\
        .limit(5)\
        .all()

    return transactions