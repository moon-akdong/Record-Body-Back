from sqlalchemy import Column, BigInteger, String, DateTime, Enum, Numeric, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Enum 
import enum
from app.core.database import Base

class NutritionSource(str, enum.Enum):
    OPEN_API = "open_api"
    AI_INFERENCE = "ai_inference"
    USER_INPUT = "user_input"

class MealRecord(Base):
    __tablename__ = "meal_records"
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger,
                     ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
                     nullable=False,
                     index=True
                     )
    eaten_at = Column(DateTime, nullable=False, index=True)
    image_url = Column(String(1000), nullable=True)
    note = Column(String(500), nullable=True)
    total_calories = Column(Numeric(10, 2), nullable=False)
    total_carb = Column(Numeric(10, 2), nullable=False, default=0)
    total_protein = Column(Numeric(10, 2), nullable=False, default=0)
    total_fat = Column(Numeric(10, 2), nullable=False, default=0)
    total_sugar = Column(Numeric(10, 2), nullable=False, default=0)

    created_at = Column(DateTime,
                        nullable=False,
                        server_default=func.now())
    updated_at = Column(DateTime,
                        nullable=False,
                        server_default=func.now(),
                        onupdate=func.now())
    
    user = relationship("User",back_populates="meal_records")
    items = relationship("MealItems",
                         back_populates="meal_record",
                         cascade="all, delete-orphan"
                         ) 
    # cascade = "all" 부모 행동을 자식에게 전파 , "delete-orphan" : 부모 행이 삭제되면 자식 행도 삭제
    __table_args__ = (
        Index("idx_meal_records_user_eaten_at", "user_id", "eaten_at"),
    ) # 복합 인덱스 
    


class MealItems(Base):
    __tablename__ = "meal_items"
    id = Column(BigInteger, primary_key = True, index=True)
    record_id = Column(BigInteger,
                       ForeignKey("meal_records.id", ondelete="CASCADE", onupdate="CASCADE"),
                       nullable=False,
                       index=True,
                       )
    food_id = Column(BigInteger,
                     ForeignKey("food.id", ondelete="CASCADE", onupdate="CASCADE"),
                     nullable =True,
                     index=True,
                     )

    name = Column(String(150), nullable=False)
    amount_g = Column(Numeric(8, 2), nullable=False)
    calories = Column(Numeric(10, 2), nullable=False)

    carb = Column(Numeric(10, 2), nullable=False, default=0)
    protein = Column(Numeric(10, 2), nullable=False, default=0)
    fat = Column(Numeric(10, 2), nullable=False, default=0)
    sugar=Column(Numeric(10, 2), nullable=False, default=0)
    confidence = Column(Numeric(5, 4), nullable=True)

    estimation_source = Column(
        Enum(NutritionSource, 
             native_enum=False,
             values_callable=lambda enum_cls: [member.value for member in enum_cls],
             # Enum 의 value가 입력되게 강제성을 부여(OPEN_API가 입력 될 수도 있다)
             ),
             nullable=False,
             default=NutritionSource.OPEN_API
    )
    crreate_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    meal_record = relationship("MealRecord", back_populates="items")
    food = relationship("Food", back_populates="meal_items")