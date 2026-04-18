from dataclasses import dataclass

@dataclass
class MealNutrients:
    food_id:int
    name:str
    amout_g:float
    calories:float
    carb:float
    protein:float
    fat:float
    sugar:float
    
class EatenNutrients:
    calories:float
    carb:float
    protein:float
    fat:float
    sugar:float
