
from dataclasses import dataclass
from datetime import datetime

@dataclass 
class FoodNutrients:
    name:str 
    food_id:int
    calories_100g:float
    carb_100g:float
    sugar_100g:float
    protein_100g:float
    fat_100g:float
    serving_size_g:float
    
class FoodCreateForm:
    name:str
    main_category:str
    sub_cateogry:str
    calories_100g:float
    carb_100g:float
    sugar_100g:float
    protein_100g:float
    fat_100g:float
    serving_size_g:float