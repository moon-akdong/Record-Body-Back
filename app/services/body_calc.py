from enum import Enum

class ActivityLevel(float, Enum):
    SEDENTARY = 1.2        # 비활동적 (운동 거의 안 함)
    LIGHT = 1.375          # 가벼운 활동 (주 1-3회)
    MODERATE = 1.55        # 보통 활동 (주 3-5회)
    ACTIVE = 1.725         # 활발한 활동 (주 6-7회)
    VERY_ACTIVE = 1.9      # 매우 활발 (운동선수 수준)

def total_daily_energy_expenditure(gender:str,
                                   age:int,
                                   weight:float,
                                   height:float,
                                   coefficient:float):
    """
    하루 총 에너지 소비량 
    """
    bmr = mifflin_formula(gender,age,weight,height)
    return bmr * coefficient

def mifflin_formula(gender:str, age:int, weight:float, height:float):
    formula = (10*weight) + (6.25*height) - (5*age) 
    if gender == 'male':
        return formula + 5
    else:
        return formula - 161

