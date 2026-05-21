from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.meal_record import MealRecord
from datetime import datetime

def period_lookup(user_id:int, start_day:datetime, end_day:datetime, db:Session):
    rows = db.query(func.date(MealRecord.eaten_at)).filter(
        MealRecord.user_id == user_id,
        MealRecord.eaten_at >= start_day,
        MealRecord.eaten_at < end_day,
    ).distinct().all()

    return rows

def month_record_lookup(user_id:int, year:int, month:int , db:Session):
    month_start = datetime(year, month, 1)

    if month == 12:
        month_end = datetime(year + 1, 1, 1)
    else:
        month_end = datetime(year, month + 1, 1)

    rows = period_lookup(user_id=user_id, start_day=month_start, end_day=month_end, db=db)
        # func.date : date(2026,5,1) 
        # .isoformat: "2026-05-01" 문자열로 변경 
    return sorted([row[0].isoformat() for row in rows])
