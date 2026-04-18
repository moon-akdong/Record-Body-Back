from pydantic import BaseModel
from datetime import datetime
class MealItemInput(BaseModel):
    food_name_kr:str
    main_category:str
    sub_category: str
    amount_g: float
class MealInput(BaseModel):
    image_url:str
    eaten_at:datetime
    note:str|None
    items: list[MealItemInput]

class MealImageResponse(BaseModel):
    file_name : str
    image_url: str
    message: str

class CreateMealResponse(BaseModel):
    user_id:int
    image_url:str
    meal_id:int