from sqlalchemy.orm import Session
from app.models.meal_record import MealRecord, MealItems
from sqlalchemy import text
from fastapi import APIRouter, Depends, HTTPException

def to_float(value):
    return float(value) if value is not None else 0.0

def read_meal_id(id:int,user_id,db:Session):
    
    query = text("""
    SELECT 
        mr.user_id,
        mr.eaten_at, 
        mr.total_calories,
        mr.total_carb,
        mr.total_protein,
        mr.total_fat,
        mr.total_sugar,
        mi.name,
        mi.amount_g,
        mi.calories,
        mi.carb,
        mi.protein,
        mi.fat,
        mi.sugar
    FROM meal_records AS mr
    JOIN meal_items AS mi ON mi.record_id = mr.id
    WHERE mr.id = :meal_id
    AND mr.user_id = :user_id
    """)

    result = db.execute(query, {
        "meal_id": id,
        "user_id": user_id
    })
    
    rows = result.mappings().all()

    return transform_meal(rows)

def transform_meal(rows):
    if not rows:
        return None

    # 1️⃣ meal 정보 (첫 row에서 추출)
    first = rows[0]

    meal = {
        "user_id": first["user_id"],
        "eaten_at": first["eaten_at"],
        "total_calories": to_float(first["total_calories"]),
        "total_carb": to_float(first["total_carb"]),
        "total_protein": to_float(first["total_protein"]),
        "total_fat": to_float(first["total_fat"]),
        "total_sugar": to_float(first["total_sugar"]),
        "items": []
    }

    # 2️⃣ items 구성
    for row in rows:
        meal["items"].append({
            "name": row["name"],
            "amount_g": to_float(row["amount_g"]),
            "calories": to_float(row["calories"]),
            "carb": to_float(row["carb"]),
            "protein": to_float(row["protein"]),
            "fat": to_float(row["fat"]),
            "sugar": to_float(row["sugar"]),
        })

    return meal