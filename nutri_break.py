def parse_food_items(text: str) -> List[FoodItem]:
    # Hardcoded nutritional database (you can expand this)
    nutrition_db = {
        "rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fats": 0.3},
        "chicken": {"calories": 165, "protein": 31, "carbs": 0, "fats": 3.6},
        "egg": {"calories": 70, "protein": 6, "carbs": 0.6, "fats": 5},
        # Add more foods
    }
    
    food_items = []
    lines = text.split('\n')
    
    for line in lines:
        food_name = line.strip().lower()
        if food_name in nutrition_db:
            nutrients = nutrition_db[food_name]
            food_items.append(FoodItem(
                name=food_name,
                calories=nutrients["calories"],
                protein=nutrients["protein"],
                carbs=nutrients["carbs"],
                fats=nutrients["fats"],
                quantity=100  # Default quantity in grams
            ))
    
    return food_items