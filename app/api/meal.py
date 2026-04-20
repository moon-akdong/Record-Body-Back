from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.user import User
from app.core.security import get_current_user
from app.core.database import get_db
from app.schemas.meal import MealInput, CreateMealResponse, MealResponse
from app.services.meal_service import register_meal_record
from app.services.meal_read import read_meal_id,read_meals_by_date
router = APIRouter(prefix="/meals", tags=["meal"])

@router.post("/register",response_model=CreateMealResponse)
def meal_create(meal_recod:MealInput, 
                       current_user : User = Depends(get_current_user),
                       db:Session = Depends(get_db)):
    meal_id = register_meal_record(user_id = current_user.id,
                                   meal_record=meal_recod,
                                   db=db)
    return {
        "user_id": current_user.id,
        "image_url": meal_recod.image_url,
        "meal_id": meal_id
    }

@router.get("/{meal_id}", response_model=MealResponse)
def meal_read(meal_id:int,
              current_user:User=Depends(get_current_user),
              db:Session=Depends(get_db)):
    meal = read_meal_id(meal_id,current_user.id,db)
    
    if not meal:
        raise HTTPException(status_code=404,detail="Meal not Found") 

    return meal

@router.get("/by-date", response_model=list[MealResponse])
def meal_eaten_read(
    eaten_at: datetime,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    meals = read_meals_by_date(eaten_at, current_user.id, db)

    return meals