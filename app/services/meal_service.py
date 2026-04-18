from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.schemas.meal import MealInput, MealItemInput
from app.domain.food import FoodNutrients
from app.domain.meal import MealNutrients, EatenNutrients
from app.services.food import get_food_nutrient
from app.models.meal_record import MealItems, MealRecord, NutritionSource

def register_meal_record(user_id:int, meal_record:MealInput,db:Session):

    existing_meal_id = find_duplicate_meal_record(user_id=user_id, eaten_at=meal_record.eaten_at,db=db)
    if existing_meal_id is not None:
        return existing_meal_id
    
    food_nutrients, missing_food = get_food_nutrient(meal_items=meal_record.items,db=db)

    nutrients_per_amount_g = calc_nutrients_per_amount_g(meal_record.items, food_nutrients)

    meal_id = create_meal_record(user_id=user_id,
                       meal_input=meal_record,
                       nutrients_per_amount_g=nutrients_per_amount_g,
                       db=db)
    return meal_id

def calc_nutrients_per_amount_g(
        meal_inputs:MealItemInput, 
        nutreints_per_100g:dict[str,FoodNutrients]
        )->dict[str,MealNutrients]:

    def calc_convert_nutritens(nutrients, serving_size, amount_g):
        return round((float(nutrients) / float(serving_size)) * float(amount_g),2)
    result: dict[str,MealNutrients] = {}

    for item in meal_inputs:
        item_name = item.food_name_kr
        food_info = nutreints_per_100g[item_name]
        if not food_info:
            # missing_food ? 
            continue
        
        result[item_name] = MealNutrients(
            food_id=food_info.food_id,
            name = food_info.name,
            amount_g=item.amount_g,
            calories= calc_convert_nutritens(food_info.calories_100g,
                                             food_info.serving_size_g, 
                                             item.amount_g),
            carb= calc_convert_nutritens(food_info.carb_100g,
                                         food_info.serving_size_g,
                                         item.amount_g),
            protein= calc_convert_nutritens(food_info.calories_100g,
                                             food_info.serving_size_g, 
                                             item.amount_g),
            fat = calc_convert_nutritens(food_info.calories_100g,
                                         food_info.serving_size_g,
                                         item.amount_g),
            sugar= calc_convert_nutritens(food_info.sugar_100g,
                                          food_info.serving_size_g,
                                          item.amount_g)
        )

    return result

def calc_one_eaten_nutrients(nutrients:dict[str,MealNutrients])->EatenNutrients:
    """
        args:
            실제 계산된 영양 정보
        returns:
            음식별 영양 별 합계

        음식별 영양 정보를 한 끼 기준 총합으로 변환한다.
    """
    calories = 0.0
    carb = 0.0
    protein = 0.0
    fat = 0.0
    sugar = 0.0
  
    for item in nutrients.values():
        calories += item.calories
        carb += item.carb
        protein += item.protein
        fat += item.fat
        sugar += item.sugar

    return EatenNutrients(
        calories=calories,
        carb=carb,
        protein=protein,
        fat=fat,
        sugar=sugar,
    )

def create_meal_record(
        user_id:int,
        meal_input:MealInput,
        nutrients_per_amount_g:dict[str,MealNutrients],
        db:Session
        ):
    one_eaten_nutrietns = calc_one_eaten_nutrients(nutrients_per_amount_g)
    meal = MealRecord(
        user_id=user_id,
        eaten_at=meal_input.eaten_at,
        image_url=meal_input.image_url,
        note=meal_input.note,
        total_calories=one_eaten_nutrietns.calories,
        total_carb=one_eaten_nutrietns.carb,
        total_protein=one_eaten_nutrietns.protein,
        total_fat=one_eaten_nutrietns.fat,
        total_sugar=one_eaten_nutrietns.sugar,
    )
    db.add(meal)
    db.flush()

    create_meal_items(nutrients=nutrients_per_amount_g, meal_id=meal.id, db=db)
    db.commit()
    db.refresh(meal)
    return meal.id

def create_meal_items(
        nutrients:dict[str,MealNutrients],
        meal_id:int,
        db:Session,
        ):
    saved_items: list[MealNutrients] = []

    for food_name, meal_nutirents in nutrients.items():
        meal_item = MealItems(
            food_id = meal_nutirents.food_id,
            record_id=meal_id,
            name=food_name,
            amount_g=meal_nutirents.amount_g,
            calories=meal_nutirents.calories,
            carb=meal_nutirents.carb,
            protein=meal_nutirents.protein,
            fat=meal_nutirents.fat,
            sugar=meal_nutirents.sugar,
            confidence=1.0,
            estimation_source=NutritionSource.OPEN_API,
        )
        db.add(meal_item)
        saved_items.append(meal_item)
    db.flush()
    return None

def find_duplicate_meal_record(
        user_id: int,
        eaten_at: datetime,
        db: Session):
    window_start = eaten_at - timedelta(minutes=5)
    window_end = eaten_at + timedelta(minutes=5)
    candidate_meals = (
        db.query(MealRecord)
        .filter(
            MealRecord.user_id == user_id,
            MealRecord.eaten_at >= window_start,
            MealRecord.eaten_at <= window_end,
        )
        .first()
    )

    if not candidate_meals:
        return None 
    
    return candidate_meals.id