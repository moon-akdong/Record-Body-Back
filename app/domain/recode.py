from dataclasses import dataclass
from datetime import datetime

@dataclass
class PeriodNutrition:
    date:datetime
    calories_sum: int 
    carb_sum: int 
    protein_sum: int 
    fat_sum:int
    sugar_sum:int
    meal_count:int
    meal_types:str

@dataclass
class DailyTdee:
    calories:float
    tdee:float
    message:str

@dataclass
class OneDayActiveLevel:
    sedentary: int   # 2100 - 1900 = +200 (잉여)
    light: int       # 2100 - 2050 = +50
    moderate: int    # 2100 - 2200 = -100 (부족)
    active: int
    very_active: int