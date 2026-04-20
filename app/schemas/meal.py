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


class MealItemResponse(BaseModel):
    name: str
    amount_g: float
    calories: float
    carb: float
    protein: float
    fat: float
    sugar: float

class MealResponse(BaseModel):
    user_id:int
    eaten_at: datetime
    total_calories: float
    total_carb: float
    total_protein: float
    total_fat: float
    total_sugar: float
    items: list[MealItemResponse]