from pydantic import BaseModel
from datetime import datetime
from app.domain.recode import OneDayActiveLevel,DailyTdee
class PeriodNutritionRequest(BaseModel):
    activity_level:str
    start_date:datetime
    end_date:datetime

class OneDayTdee(BaseModel):
    total_calories:float
    levels: OneDayActiveLevel
    message:str

class PeriodTdee(BaseModel):
    date:str
    daily_tdee:DailyTdee