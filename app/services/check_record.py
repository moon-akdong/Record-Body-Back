from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.meal_record import MealRecord
from datetime import datetime

from app.domain.recode import DailyNutritionSummary

def get_recorded_dates(user_id:int, start_day:datetime, end_day:datetime, db:Session):
    """기간 내 식사 기록이 존재하는 날짜 목록을 중복 없이 조회한다.
    반환 예시: [(datetime.date(2026, 5, 20),), (datetime.date(2026, 5, 22),)]
    """
    rows = db.query(func.date(MealRecord.eaten_at)).filter(
        MealRecord.user_id == user_id,
        MealRecord.eaten_at >= start_day,
        MealRecord.eaten_at < end_day,
    ).distinct().all()

    return rows

def get_daily_nutrition_summary(user_id:int, start_day:datetime, end_day:datetime, db:Session) -> list[DailyNutritionSummary]:
    """기간 내 일별 영양소(칼로리, 탄수화물, 단백질, 지방, 당류) 합계를 조회한다.
    반환 예시: [(datetime.date(2026, 5, 20), 2100, 250, 80, 60, 30), ...]
    순서: (날짜, 칼로리, 탄수화물, 단백질, 지방, 당류)
    """
    rows = db.query(
      func.date(MealRecord.eaten_at),
      func.sum(MealRecord.total_calories),
      func.sum(MealRecord.total_carb),
      func.sum(MealRecord.total_protein),
      func.sum(MealRecord.total_fat),
      func.sum(MealRecord.total_sugar),
      func.count(MealRecord.id),
      func.group_concat(MealRecord.meal_type),
        ).filter(
            MealRecord.user_id == user_id,
            MealRecord.eaten_at >= start_day,
            MealRecord.eaten_at < end_day,
        ).group_by(func.date(MealRecord.eaten_at)).all()

    return [
        DailyNutritionSummary(
            date=row[0],
            calories_sum=row[1],
            carb_sum=row[2],
            protein_sum=row[3],
            fat_sum=row[4],
            sugar_sum=row[5],
            meal_count=row[6],
            meal_types=row[7],
        ) for row in rows
    ]

def get_monthly_recorded_dates(user_id:int, year:int, month:int, db:Session):
    """특정 월에 식사 기록이 존재하는 날짜를 ISO 문자열 리스트로 반환한다.
    반환 예시: ["2026-05-01", "2026-05-03", "2026-05-20"]
    """
    month_start = datetime(year, month, 1)

    if month == 12:
        month_end = datetime(year + 1, 1, 1)
    else:
        month_end = datetime(year, month + 1, 1)

    rows = get_recorded_dates(user_id=user_id, start_day=month_start, end_day=month_end, db=db)
    return sorted([row[0].isoformat() for row in rows])

def get_period_nutrition_summary(user_id:int, start_day:datetime, end_day:datetime, db:Session) -> list[DailyNutritionSummary]:
    """지정 기간의 일별 영양소 합계를 조회한다.
    반환: list[DailyNutritionSummary]
    """
    return get_daily_nutrition_summary(user_id=user_id, start_day=start_day, end_day=end_day, db=db)

def get_monthly_nutrition_summary(user_id:int, year:int, month:int, db:Session) -> list[DailyNutritionSummary]:
    """특정 월의 일별 영양소 합계를 조회한다.
    반환: list[DailyNutritionSummary]
    """
    month_start = datetime(year, month, 1)

    if month == 12:
        month_end = datetime(year + 1, 1, 1)
    else:
        month_end = datetime(year, month + 1, 1)

    return get_daily_nutrition_summary(user_id=user_id, start_day=month_start, end_day=month_end, db=db)
