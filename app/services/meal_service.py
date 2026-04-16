from sqlalchemy.orm import Session

from app.schemas.meal import MealInput, MealItemInput

def create_meal_record(user_id:int,
                       meal_input:MealInput,
                       db):
    """
    args:
        user_id, meal_input, db
    returns: 
        {eaten_at, mealrecord.id, }
    Food 정보를 가져와서, MealRecord에 저장 후 MealItem에 저장 

    """
    pass 