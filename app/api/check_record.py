from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.core.security import get_current_user
from app.services.check_record import get_monthly_recorded_dates
from app.schemas.meal import MonthRecord
from app.schemas.recode import PeriodNutritionRequest, OneDayTdee
from datetime import datetime
from app.services.body_calc import CalorieManager
from app.schemas.recode import PeriodNutritionRequest, OneDayTdee, PeriodTdee

router = APIRouter(prefix="/check_record", tags=["check_record"])

@router.get("/month_record",response_model=MonthRecord)
def check_month(year:int,
                month:int, 
                current_user:User = Depends(get_current_user),
                db:Session = Depends(get_db)):
    
    month_record = get_monthly_recorded_dates(user_id=current_user.id,
                                      year=year,
                                      month=month,
                                      db=db)
    return {"month":month_record}

@router.post("/period_tdee", response_model=list[PeriodTdee])
def get_period_tdee(
    request:PeriodNutritionRequest,
    current_user:User = Depends(get_current_user),
    db:Session = Depends(get_db)):
    
    cal_manager = CalorieManager(user=current_user, db=db)

    return cal_manager.get_period_balance(**request.model_dump())

@router.post("/day_tdee", response_model=OneDayTdee)
def get_day_tdee(date:datetime, 
                    current_user:User=Depends(get_current_user),
                    db:Session=Depends(get_db)):
    
    cal_manager = CalorieManager(user=current_user, db=db)
    return cal_manager.get_balance(date)