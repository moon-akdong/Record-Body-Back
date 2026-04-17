from sqlalchemy.orm import Session

from app.schemas.meal import MealInput, MealItemInput
from app.domain.food import FoodNutrients
from app.domain.meal import MealNutrients, EatenNutrients
from app.services.food import get_food_nutrient

def create_meal_record(user_id:int, meal_record:MealInput,db:Session):
    food_nutrients, missing_food = get_food_nutrient(meal_items=meal_record.items)
    nutrients_per_amount_g = calc_nutrients_per_amount_g(meal_record.items, food_nutrients)
    one_eaten_nutrietns = calc_one_eaten_nutrients(nutrients_per_amount_g)


def calc_nutrients_per_amount_g(
        meal_inputs:MealItemInput, 
        nutreints_per_100g:dict[str,FoodNutrients]
        )->dict[str,MealNutrients]:

    def calc_convert_nutritens(nutrients, serving_size, amount_g):
        return (float(nutrients) / float(serving_size)) * float(amount_g)
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
            amout_g=item.amount_g,
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

    return MealNutrients(
        calories=calories,
        carb=carb,
        protein=protein,
        fat=fat,
        sugar=sugar,
    )
