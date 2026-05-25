from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.core.security import get_current_user
from app.services.check_record import get_monthly_recorded_dates
from app.schemas.meal import MonthRecord
from app.schemas.recode import PeriodNutritionRequest

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

