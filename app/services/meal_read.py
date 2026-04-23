from sqlalchemy.orm import Session
from app.models.meal_record import MealRecord, MealItems
from sqlalchemy import text
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta

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

def read_meals_by_date(eaten_at: datetime, user_id: int, db: Session):
    start = eaten_at.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)

    query = text("""
    SELECT 
        mr.id AS meal_id,
        mr.user_id,
        mr.eaten_at,
        mr.total_calories,
        mr.total_carb,
        mr.total_protein,
        mr.total_fat,
        mr.total_sugar,
        mr.image_url
        mi.name,
        mi.amount_g,
        mi.calories,
        mi.carb,
        mi.protein,
        mi.fat,
        mi.sugar
    FROM meal_records AS mr
    JOIN meal_items AS mi ON mi.record_id = mr.id
    WHERE mr.user_id = :user_id
    AND mr.eaten_at >= :start
    AND mr.eaten_at < :end
    ORDER BY mr.eaten_at DESC
    """)

    result = db.execute(query, {
        "user_id": user_id,
        "start": start,
        "end": end
    })

    rows = result.mappings().all()

    return transform_meal_list(rows)

def transform_meal_list(rows):
    if not rows:
        return []

    meal_map = {}

    for row in rows:
        meal_id = row["meal_id"]

        if meal_id not in meal_map:
            meal_map[meal_id] = {
                "meal_id": int(row["meal_id"]),
                "user_id": int(row["user_id"]),
                "eaten_at": row["eaten_at"],
                "image_url" : row["image_url"],
                "total_calories": to_float(row["total_calories"]),
                "total_carb": to_float(row["total_carb"]),
                "total_protein": to_float(row["total_protein"]),
                "total_fat": to_float(row["total_fat"]),
                "total_sugar": to_float(row["total_sugar"]),
                "items": []
            }

        meal_map[meal_id]["items"].append({
            "name": row["name"],
            "amount_g": to_float(row["amount_g"]),
            "calories": to_float(row["calories"]),
            "carb": to_float(row["carb"]),
            "protein": to_float(row["protein"]),
            "fat": to_float(row["fat"]),
            "sugar": to_float(row["sugar"]),
        })

    return list(meal_map.values())