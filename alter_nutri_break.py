import requests
from typing import Optional

API_KEY = "YOUR_USDA_API_KEY"  # Get from https://fdc.nal.usda.gov/api-key-signup.html
USDA_API_URL = "https://api.nal.usda.gov/fdc/v1"

def get_nutrition_data(food_name: str) -> Optional[Dict]:
    try:
        # Search for food
        search_url = f"{USDA_API_URL}/foods/search"
        params = {
            "api_key": API_KEY,
            "query": food_name,
            "dataType": ["SR Legacy", "Foundation", "Survey (FNDDS)"],
            "pageSize": 1
        }
        
        response = requests.get(search_url, params=params)
        data = response.json()
        
        if data["foods"]:
            food = data["foods"][0]
            nutrients = food["foodNutrients"]
            
            return {
                "name": food_name,
                "calories": next((n["value"] for n in nutrients if n["nutrientName"] == "Energy"), 0),
                "protein": next((n["value"] for n in nutrients if n["nutrientName"] == "Protein"), 0),
                "carbs": next((n["value"] for n in nutrients if n["nutrientName"] == "Carbohydrate, by difference"), 0),
                "fats": next((n["value"] for n in nutrients if n["nutrientName"] == "Total lipid (fat)"), 0)
            }
        return None
    except Exception as e:
        print(f"Error fetching nutrition data for {food_name}: {e}")
        return None

def parse_food_items(text: str) -> List[FoodItem]:
    food_items = []
    lines = text.split('\n')
    
    for line in lines:
        food_name = line.strip()
        nutrition_data = get_nutrition_data(food_name)
        
        if nutrition_data:
            food_items.append(FoodItem(
                name=food_name,
                calories=nutrition_data["calories"],
                protein=nutrition_data["protein"],
                carbs=nutrition_data["carbs"],
                fats=nutrition_data["fats"],
                quantity=100  # Default quantity in grams
            ))
    
    return food_items