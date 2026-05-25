from pydantic import BaseModel
from datetime import datetime

class PeriodNutritionRequest(BaseModel):
    activity_level:str
    start_date:datetime
    end_date:datetime