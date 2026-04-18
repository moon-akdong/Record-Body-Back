from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import get_current_user
from app.core.database import get_db
from app.schemas.meal import MealInput
from app.services.meal_service import register_meal_record
router = APIRouter(prefix="/meals", tags=["meal"])

@router.post("/register")
def meal_create(meal_recod:MealInput, 
                       current_user : User = Depends(get_current_user),
                       db:Session = Depends(get_db)):
    meal_id = register_meal_record(user_id = current_user.id,
                                   meal_input=meal_recod,
                                   db=db)
    return {
        "user_id": current_user.id,
        "image_url": meal_recod.image_url,
        "meal_id": meal_id
    }