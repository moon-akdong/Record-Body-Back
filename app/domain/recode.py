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