from sqlalchemy import Column, BigInteger, String, DateTime, Enum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
from app.core.database import Base


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    
class UserRole(str, Enum):
    """DB·API에서 쓰는 role 문자열과 동일하게 유지."""
    SUPER_MANAGER = "super_manager"
    MANAGER = "manager"
    USER = "user"

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    birth_date = Column(DateTime, nullable=False)
    gender = Column(Enum(Gender, 
                         native_enum=False,
                         values_callable=lambda enum_cls: [member.value for member in enum_cls],
                         ), 
                    nullable=False)

    height = Column(Numeric(5, 2), nullable=False)
    weight = Column(Numeric(5, 2), nullable=False)
    role = Column(Enum(UserRole, 
                       native_enum=False,
                       values_callable=lambda enum_cls: [member.value for member in enum_cls],
                       ),
                  nullable=False,
                  default=UserRole)
    
    created_at = Column(DateTime,
                        nullable=False,
                        server_default=func.now())
    updated_at = Column(DateTime,
                        nullable=False,
                        server_default=func.now(),
                        onupdate=func.now())

    meal_records = relationship("MealRecord", 
                                back_populates="user", 
                                cascade="all, delete-orphan")

