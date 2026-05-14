from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.meal_record import MealRecord
from datetime import datetime

def check_month_record(user_id:int, year:int, month:int , db:Session):
    month_start = datetime(year, month, 1)

    if month == 12:
        month_end = datetime(year + 1, 1, 1)
    else:
        month_end = datetime(year, month + 1, 1)

    rows = db.query(func.date(MealRecord.eaten_at)).filter(
        MealRecord.user_id == user_id,
        MealRecord.eaten_at >= month_start,
        MealRecord.eaten_at < month_end,
    ).distinct().all()
        # func.date : date(2026,5,1) 
        # .isoformat: "2026-05-01" 문자열로 변경 
    return sorted([row[0].isoformat() for row in rows])