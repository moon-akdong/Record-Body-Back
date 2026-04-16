import requests

from app.core.config import settings
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

