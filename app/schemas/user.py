from pydantic import BaseModel, EmailStr
from datetime import date
from models.user import Gender
# EmailStr : pip install email-validator, 내부에서 email_calidator에 의존적이기 때문에

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    birth_date:date
    gender:Gender # male, female
    height:float
    weight:float

class UserLogin(BaseModel):
    email: EmailStr
    password: str
