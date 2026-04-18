from dataclasses import dataclass

@dataclass
class MealNutrients:
    food_id:int
    name:str
    amount_g:float
    calories:float
    carb:float
    protein:float
    fat:float
    sugar:float

@dataclass
class EatenNutrients:
    calories:float
    carb:float
    protein:float
    fat:float
    sugar:float
