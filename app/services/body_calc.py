
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

