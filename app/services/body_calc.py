from enum import Enum
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.check_record import CaloriesLog
from app.services.calc import calc_age
from app.schemas.recode import OneDayTdee, PeriodTdee
from app.domain.recode import DailyTdee, DailyTdee,OneDayActiveLevel

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
ACTIVITY_LEVELS = ["sedentary", "light", "moderate", "active", "very_active"]

class Tdee:
    def __init__(self, user:User):
        self.gender = str(user.gender)
        self.weight = float(user.weight)
        self.height = float(user.height)
        self.age = calc_age(user.birth_date)
    
    def calc_activity(self, activity_level):
        
        aw = ActivityLevel[activity_level.upper()]
        tdee = self._total_daily_energy_expenditure(gender=self.gender,
                                            age=self.age,
                                            weight=self.weight,
                                            height=self.height,
                                            activate_weight=aw
                                            )
        return tdee

    def _calc_bmr_mifflin_formula(
            self,
            gender:str,
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
        
    def _total_daily_energy_expenditure(
            self,
            gender:str,
            age:int,
            weight:float,
            height:float,
            activate_weight:float) -> float:
        
        """
        하루 총 에너지 소비량 
        """
        bmr = self._calc_bmr_mifflin_formula(gender=gender,
                            age=age,
                            weight=weight,
                            height=height)
        
        return bmr * activate_weight

class CalorieManager:
    def __init__(self,user:User, db:Session):
        
        self.tdee = Tdee(user)
        self.log = CaloriesLog(user.id,db)

    def _build_daily_tdee(self, intake, activity_level) -> DailyTdee:
        return DailyTdee(
            calories=intake.calories_sum,
            tdee=round(float(intake.calories_sum) - self._get_daily_tdee(activity_level),2),
            message=self._daily_message(intake.meal_types, intake.meal_count)
        )
    
    def get_period_balance(self,start_date,end_date,activity_level)-> list[PeriodTdee]:

        intakes = self.log.fetch_calorie_period(start_date=start_date, end_date=end_date)
        results = []
        for intake in intakes:
            results.append(PeriodTdee(
                date=str(intake.date),
                daily_tdee=self._build_daily_tdee(intake, activity_level)
            ))
        return results

    def get_balance(self,today) -> OneDayTdee:
        intake = self.log.fetch_calorie(today=today)

        if intake is None:
            return None
        
        message = self._daily_message(intake.meal_types, intake.meal_count)
        activity_levels_tdee = {}

        for val in ACTIVITY_LEVELS:
            activity_levels_tdee[val] = round(float(intake.calories_sum) - self._get_daily_tdee(val),2)

        return OneDayTdee(
            total_calories=intake.calories_sum,
            levels=OneDayActiveLevel(**activity_levels_tdee),
            message = message
            )
    
    def _get_daily_tdee(
            self,
            activity_level:str):
        tdee = self.tdee.calc_activity(activity_level=activity_level)
        return float(tdee)
    
    def _daily_message(self, meal_types: str, meal_count: int) -> str:
        if not meal_types:
            return f"{meal_count}끼 식사 기록"
        kr_types = ",".join(MEAL_TYPE_KR[t] for t in meal_types.split(","))
        return f"{kr_types} 기록"
    
