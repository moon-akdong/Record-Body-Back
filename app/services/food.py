from sqlalchemy.orm import Session
from typing import Tuple
import logging
from app.schemas.meal import MealItemInput
from app.domain.food import FoodNutrients, FoodCreateForm
from app.services.openapi_food import fetch_food_date
from app.models.food import FoodMainCategory, FoodSubCategory, Food

logger = logging.getLogger(__name__)

def get_food_nutrient(meal_items:list[MealItemInput],
                   db:Session): 
    food_map:  dict[str, FoodNutrients] = {}

    missing = [] 
    food_items, missing_names = _get_table_nutrient(meal_items,db)
    food_map = food_items.copy()

    table_missing = list(item for item in meal_items if item.food_name_kr in missing_names)
    
    for item in table_missing:
        food_item = _fetch_api_nutrient(item,db) 
        if food_item is None:
            missing.append(item)
            continue
        food_map[item.food_name_kr] = food_item

    return food_map, missing
        
def _get_table_nutrient(meal_items:list[MealItemInput],
                    db) -> Tuple[dict[str, FoodNutrients], list[str]]:
    """
    args:
        입력된 리스트 
    returns:
        내부 DB Table에 있는 데이터(dict), 없는 데이터(list)
    """
    names = list(item.food_name_kr for item in meal_items)

    foods = (
        db.query(Food)
        .filter(Food.food_name_kr.in_(names))
        .all()
        ) # 없는 건 안나옴 

    food_map = {
        food.food_name_kr: food for food in foods
        }
    
    result = {
        name: FoodNutrients(
            food_id=food.id,
            name=food.food_name_kr,
            calories_100g=food.calories_100g,
            carb_100g=food.carb_per_100g,
            sugar_100g=food.sugar_per_100g,
            protein_100g=food.protein_per_100g,
            fat_100g=food.fat_per_100g,
            serving_size_g=food.serving_size_g,
            )
            for name, food in food_map.items()
        }
    missing_names = [
        name for name in names
        if name not in food_map
        ]
    
    return result, missing_names


def _fetch_api_nutrient(item:MealItemInput, db:Session) -> FoodNutrients:
    try:
        openapi_data =fetch_food_date(meal_item=item, db=db)

    except Exception:
        logger.exception(
            "OpenAPI 연결 실패"
        )
        return None 

    if openapi_data is None:
        logger.warning(
            "OpenAPI에서 음식 정보를 찾을 수 없음 : food_name=%s, main_category=%s, sub_category=%s",
            item.food_name_kr,
            item.main_category,
            item.sub_category,
        )
        return None 

    food_id = _get_or_create_food(openapi_data, db)

    return FoodNutrients(
        name=openapi_data.name,
        food_id=food_id,
        calories_100g=openapi_data.calories_100g,
        carb_100g=openapi_data.carb_100g,
        protein_100g=openapi_data.protein_100g,
        sugar_100g=openapi_data.sugar_100g,
        fat_100g=openapi_data.fat_100g,
        serving_size_g=openapi_data.serving_size_g
    )

def _get_or_create_food(data:FoodCreateForm, db:Session) -> int:
    existing_food = db.query(Food).filter(Food.name == data.name).first()
    if existing_food is not None:
        return existing_food
    
    main_category_id = _get_or_create_category(table=FoodMainCategory,category_name=data.main_category, db=db)
    sub_category_id = _get_or_create_category(table=FoodSubCategory,category_name=data.sub_cateogry,db=db)
    
    food = Food(
        name=data.name,
        main_category_id=main_category_id,
        sub_category_id=sub_category_id,
        calories_per_100g=data.calories_per_100g,
        carb_per_100g=data.carb_per_100g,
        sugar_per_100g=data.sugar_per_100g,
        protein_per_100g=data.protein_per_100g,
        fat_per_100g=data.fat_per_100g,
        serving_size_g=data.serving_size_g,
    )
    db.add(food)
    db.commit()
    db.refresh(food)
    return food.id

    

def _get_or_create_category(table, category_name: str, db: Session) -> int:
    category = db.query(table).filter(table.name == category_name).first()
    if category is not None:
        return category.id

    category = table(name=category_name)
    db.add(category)
    db.flush()
    return category.id

