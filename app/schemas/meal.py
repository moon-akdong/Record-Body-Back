from pydantic import BaseModel
from datetime import datetime

def MealInput(BaseModel):
    image_url:str
    eaten_at:datetime
    note:str|None
    items: list[MealItemInput]

def MealItemInput(BaseModel):
    food_name_kr:str
    main_category:str
    sub_category: str
    amount_g: float

def MealImageResponse(BaseModel):
    file_name : str
    image_url: str
    message: str