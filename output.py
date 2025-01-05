from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional
from PyPDF2 import PdfReader
import re

@dataclass
class FoodItem:
    name: str
    calories: float
    protein: float
    carbs: float
    fats: float
    quantity: float

class DietCalculator:
    def calculate_calories(self, user: UserProfile) -> Dict[str, float]:
        # Basic BMR calculation using Mifflin-St Jeor Equation
        if user.gender.lower() == "male":
            bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age + 5
        else:
            bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age - 161

        # Adjust based on health goal
        if user.health_goal == HealthGoal.FAT_LOSS:
            calories = bmr * 0.85  # 15% deficit
            macros = {"protein": user.weight * 2.2, "carbs": calories * 0.4 / 4, "fats": calories * 0.25 / 9}
        elif user.health_goal == HealthGoal.MUSCLE_BUILDING:
            calories = bmr * 1.15  # 15% surplus
            macros = {"protein": user.weight * 2.4, "carbs": calories * 0.45 / 4, "fats": calories * 0.25 / 9}
        else:  # SEDENTARY
            calories = bmr
            macros = {"protein": user.weight * 1.8, "carbs": calories * 0.45 / 4, "fats": calories * 0.3 / 9}
        
        macros["calories"] = calories
        return macros

def parse_food_items(text: str) -> List[FoodItem]:
    food_items = []
    lines = text.split('\n')
    for line in lines:
        try:
            name, cals, prot, carbs, fats, qty = line.strip().split(',')
            food_items.append(FoodItem(
                name=name.strip(),
                calories=float(cals),
                protein=float(prot),
                carbs=float(carbs),
                fats=float(fats),
                quantity=float(qty)
            ))
        except ValueError:
            continue
    return food_items

def suggest_diet(user: UserProfile, food_items: List[FoodItem]) -> Dict:
    calculator = DietCalculator()
    targets = calculator.calculate_calories(user)
    
    diet_plan = {
        "breakfast": [],
        "lunch": [],
        "dinner": [],
        "snacks": []
    }
    
    current = {"calories": 0, "protein": 0, "carbs": 0, "fats": 0}
    
    # Distribution across meals
    meal_ratios = {
        "breakfast": 0.25,
        "lunch": 0.35,
        "dinner": 0.3,
        "snacks": 0.1
    }
    
    for meal, ratio in meal_ratios.items():
        meal_targets = {k: v * ratio for k, v in targets.items()}
        
        for food in food_items:
            if food.quantity <= 0:
                continue
                
            portion = min(
                food.quantity,
                (meal_targets["calories"] - current["calories"]) / food.calories if food.calories > 0 else 0
            )
            
            if portion > 0:
                diet_plan[meal].append({
                    "food": food.name,
                    "portion": round(portion, 2)
                })
                
                current["calories"] += food.calories * portion
                current["protein"] += food.protein * portion
                current["carbs"] += food.carbs * portion
                current["fats"] += food.fats * portion
    
    is_deficit = any(current[nutrient] < targets[nutrient] * 0.9 for nutrient in current)
    
    return {
        "plan": diet_plan,
        "targets": targets,
        "achieved": current,
        "is_deficit": is_deficit
    }

def main():
    user = get_user_input()
    pdf_path = input("Enter path to food items PDF: ")
    
    raw_text = extract_pdf_text(pdf_path)
    food_items = parse_food_items(raw_text)
    
    diet_result = suggest_diet(user, food_items)
    
    print("\nDiet Recommendations:")
    if diet_result["is_deficit"]:
        print("WARNING: Cannot meet nutritional requirements with available foods")
    
    for meal, foods in diet_result["plan"].items():
        print(f"\n{meal.title()}:")
        for item in foods:
            print(f"- {item['food']}: {item['portion']}g")
    
    print("\nNutritional Summary:")
    for nutrient, amount in diet_result["achieved"].items():
        target = diet_result["targets"][nutrient]
        print(f"{nutrient}: {amount:.1f}/{target:.1f}")

if __name__ == "__main__":
    main()