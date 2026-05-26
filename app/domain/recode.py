from dataclasses import dataclass
from datetime import datetime

@dataclass
class DailyNutritionSummary:
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
    date:datetime
    tdee_info:float
    message:str

