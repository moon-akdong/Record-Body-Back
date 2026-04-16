import requests
from sqlalchemy.orm import Session

from app.core.config import settings
from app.domain.food import FoodCreateForm
from app.schemas.meal import MealItemInput
# from app.schemas

FOOD_DB_ENDPOINT = f"{settings.food_db_url}/getFoodNtrCpntDbInq02"
def _normalize_text(text: str | None) -> str:
    if text is None:
        return ""
    return text.replace(" ", "").replace("_", "").lower().strip()

def get_food_db_data(
    food_name: str,
    sub_cateogry: str | None = None,
    page_no: int = 1,
    num_of_rows: int = 30,
) -> dict:
    params = {
        "serviceKey": settings.food_db_key,
        "pageNo": page_no,
        "numOfRows": num_of_rows,
        "type": "json",
        "FOOD_NM_KR": _normalize_text(food_name),
    }
    if sub_cateogry:
        params["FOOD_CAT1_NM"] = sub_cateogry
    
    response = requests.get(FOOD_DB_ENDPOINT, params=params, timeout=30)
    response.raise_for_status()
    return response.json()
    
def _to_float(value: str | None) -> float:
    if value in (None, ""):
        return 0.0
    return float(value)

def _gram_to_float(value: str | None) -> float:
      if not value:
          return 100.0

      normalized = value.strip().lower()
      if normalized.endswith("g"):
          return float(normalized[:-1].strip())

      return 100.0

def filter_food_item(
    items: list[dict],
    food_name: str,
    main_category: str | None = None,
    sub_category: str | None = None,
) -> dict | None:
    normalized_food_name = _normalize_text(food_name)
    normalized_main_category = _normalize_text(main_category)
    normalized_sub_category = _normalize_text(sub_category)

    exact_matches = [
        item
        for item in items
        if _normalize_text(item.get("FOOD_NM_KR")) == normalized_food_name
        and (
            not normalized_main_category
            or _normalize_text(item.get("FOOD_OR_NM")) == normalized_main_category
        )
        and (
            not normalized_sub_category
            or _normalize_text(item.get("FOOD_CAT1_NM")) == normalized_sub_category
        )
    ]
    if exact_matches:
        return exact_matches[0]

    exact_name_matches = [
        item
        for item in items
        if _normalize_text(item.get("FOOD_NM_KR")) == normalized_food_name
    ]
    if exact_name_matches:
        return exact_name_matches[0]

    contains_matches = [
        item
        for item in items
        if normalized_food_name in _normalize_text(item.get("FOOD_NM_KR"))
        or _normalize_text(item.get("FOOD_NM_KR")) in normalized_food_name
    ]
    if contains_matches:
        return contains_matches[0]

    return None

def fetch_food_date(meal_item:MealItemInput,db:Session):
    food_infos_json = get_food_db_data(food_name=meal_item.food_name_kr,
                     sub_cateogry=meal_item.sub_category)
    items = food_infos_json.get("body",{}).get("items",[])
    if not items:
        return None
    
    item = filter_food_item(items, food_name=meal_item.food_name_kr, 
                            main_category=meal_item.main_category,
                            sub_category = meal_item.sub_category)

    if item is None:
        return None
    
    return FoodCreateForm(
            name=item.get("FOOD_NM_KR", meal_item.food_name_kr),
            main_category=item.get("FOOD_OR_NM", meal_item.main_category),
            sub_category=item.get("FOOD_CAT1_NM", meal_item.sub_category),
            calories_100g=_to_float(item.get("AMT_NUM1")),
            water_g=_to_float(item.get("AMT_NUM2")),
            carb_per_g=_to_float(item.get("AMT_NUM5")),
            protein_per_g=_to_float(item.get("AMT_NUM3")),
            fat_per_g=_to_float(item.get("AMT_NUM4")),
            sugar_per_g=_to_float(item.get("AMT_NUM7")),
            serving_size_g=_gram_to_float(item.get("SERVING_SIZE"))
        )