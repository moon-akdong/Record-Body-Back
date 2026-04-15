from sqlalchemy import Column, BigInteger, String, DateTime, Enum, Numeric, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

class Food(Base):
    __tablename__= "food"
    id =Column(BigInteger, primary_key=True, index=True)
    name = Column(String(150), nullable=False, unique=True, index=True)
    main_category_id = Column(BigInteger,
                              ForeignKey(
                                  "food_main_categories.id",
                                  ondelete="SET NULL",
                                  onupdate="CASCADE",
                              ),
                              nullable=True,
                              )
    sub_category_id = Column(BigInteger,
                             ForeignKey(
                                 "food_sub_cateories.id",
                                 ondelete="SET NULL",
                                 onupdate="CASCADE",
                             ),
                             nullable=True,
                             )
    
    calories_per_100g = Column(Numeric(8, 2), nullable=False)
    carb_per_100g = Column(Numeric(8, 2), nullable=False, default=0)
    sugar_per_100g = Column(Numeric(8, 2), nullable=False, default=0)
    protein_per_100g = Column(Numeric(8, 2), nullable=False, default=0)
    fat_per_100g = Column(Numeric(8, 2), nullable=False, default=0)
    serving_size_g = Column(Numeric(8, 2), nullable=True)
    created_at = Column(DateTime,
                        nullable=False,
                        server_default=func.now())
    updated_at = Column(DateTime,
                        nullable=False,
                        server_default=func.now(),
                        onupdate=func.now())
    
    meal_items = relationship("MealItems",
                              back_populates="food",
                              passive_deletes=True)
    # passive_deletes = True : 삭제 연쇄 처리를 SQLAlchemy가 아니라 DB 외래키 규칙으로 맡기겠다
    main_category = relationship("FoodMainCategory",
                                 back_populates="food")
    
    sub_category = relationship("FoodSubCategory",
                                back_populates="food")

    __table_args__=(
        Index("idx_food_main_category_id", "main_category_id"),
        Index("idx_foods_sub_category_id", "sub_category_id"),
    )

class FoodMainCategory(Base):
    __tablename__ = "food_main_categories"
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime,
                        nullable=False,
                        server_default=func.now())

    food = relationship("Food",
                        back_populates = "main_category",
                        passtive_deletes=True,
                        )
    
class FoodSubCategory(Base):
    __tablename__ = "food_sub_categories"
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime,
                        nullable=False,
                        server_default=func.now())

    food = relationship("Food",
                        back_populates = "sub_cateogory",
                        passtive_deletes=True,
                        )