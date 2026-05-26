from enum import Enum
from collections import defaultdict
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.check_record import get_daily_nutrition_summary
from app.services.calc import calc_age
from app.schemas.recode import PeriodNutritionRequest
from app.domain.recode import DailyNutritionSummary, DailyTdee
from collections.abc import MutableMapping

class ActivityLevel(float, Enum):
    SEDENTARY = 1.2        # 비활동적 (운동 거의 안 함)
    LIGHT = 1.375          # 가벼운 활동 (주 1-3회)
    MODERATE = 1.55        # 보통 활동 (주 3-5회)
    ACTIVE = 1.725         # 활발한 활동 (주 6-7회)
    VERY_ACTIVE = 1.9      # 매우 활발 (운동선수 수준)

MEAL_TYPE_KR = {
    "breakfast": "아침",
    "lunch": "점심",
    "dinner": "저녁",
    "snack": "간식",
    "night": "야식",
}

def total_daily_energy_expenditure(gender:str,
                                   age:int,
                                   weight:float,
                                   height:float,
                                   activate_weight:float) -> float:
    """
    하루 총 에너지 소비량 
    """
    bmr = mifflin_formula(gender=gender,
                          age=age,
                          weight=weight,
                          height=height)
    
    return bmr * activate_weight

def mifflin_formula(gender:str,
                    age:int,
                    weight:float,
                    height:float) -> float:

    MALE_WEIGHT = 5
    FEMALE_WEIGHT = 161
    
    formula = (10*weight) + (6.25*height) - (5*age) 
    if gender == 'male':
        return formula + MALE_WEIGHT
    else:
        return formula - FEMALE_WEIGHT

def period_tdee(request:PeriodNutritionRequest,
                user:User,
                db:Session):
    tdee = calc_tdee(request.activity_level,user)
    period_info = get_daily_nutrition_summary(user.id, 
                                              start_day=request.start_date, 
                                              end_day=request.end_date,
                                              db=db)
    return calc_period_tdee(period_info,tdee)

def calc_tdee(activity_level, user:User):
    birth_day = user.birth_date
    age = calc_age(birth_day)
    aw = ActivityLevel[activity_level.upper()]

    tdee = total_daily_energy_expenditure(gender=user.gender,
                                          age=age,
                                          weight=user.weight,
                                          height=user.height,
                                          activate_weight=aw
                                          )
    return tdee
    
def calc_period_tdee(period_calories:list[DailyNutritionSummary],
                     tdee:int)->dict[str,DailyTdee]:
    result = {}
    for pc in period_calories:
        result[str(pc.date)] = DailyTdee(
            date=pc.date,
            tdee_info=pc.calories_sum - tdee,
            message=daily_message(pc.meal_types,pc.meal_count)
        )
    return result

def daily_message(meal_types:str, meal_count:int) -> str:
    kr_types = ",".join(MEAL_TYPE_KR[t] for t in meal_types.split(",")) 
    return f"{meal_count}끼 {kr_types} 식사 기록"