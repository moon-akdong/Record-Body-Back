from pydantic import BaseModel
from datetime import datetime
from app.models.meal_record import MealType
class MealItemInput(BaseModel):
    food_name_kr:str
    category: str
    amount_g: float
class MealInput(BaseModel):
    meal_type:MealType
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
    id:int
    user_id:int
    eaten_at: datetime
    image_url:str | None
    meal_type:MealType
    total_calories: float
    total_carb: float
    total_protein: float
    total_fat: float
    total_sugar: float
    note:str | None
    items: list[MealItemResponse]


class SubCategoryResponse(BaseModel):
    name:str

class MonthRecord(BaseModel):
    month:list[str]