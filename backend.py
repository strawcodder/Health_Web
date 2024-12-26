from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional
import json

class HealthGoal(Enum):
    FAT_LOSS = "fat loss"
    SEDENTARY = "sedentary life style"
    MUSCLE_BUILDING = "muscle building"

@dataclass
class UserProfile:
    height: float  # in cm
    weight: float  # in kg
    age: int
    gender: str
    health_goal: HealthGoal
    
    def calculate_bmi(self) -> float:
        return self.weight / ((self.height/100) ** 2)
    
    def get_recommendations(self) -> Dict[str, str]:
        bmi = self.calculate_bmi()
        recommendations = {
            "bmi": f"Your BMI is: {bmi:.1f}",
            "category": self._get_bmi_category(bmi),
            "goal_specific": self._get_goal_recommendations()
        }
        return recommendations
    
    def _get_bmi_category(self, bmi: float) -> str:
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def _get_goal_recommendations(self) -> str:
        if self.health_goal == HealthGoal.FAT_LOSS:
            return "Focus on caloric deficit and regular cardio exercise"
        elif self.health_goal == HealthGoal.SEDENTARY:
            return "Try to incorporate more movement and regular stretching"
        else:  # MUSCLE_BUILDING
            return "Ensure adequate protein intake and progressive resistance training"

def get_user_input() -> UserProfile:
    print("\nEnter your health profile information:")
    height = float(input("Height (in cm): "))
    weight = float(input("Weight (in kg): "))
    age = int(input("Age: "))
    gender = input("Gender: ")
    
    print("\nSelect your health goal:")
    for i, goal in enumerate(HealthGoal, 1):
        print(f"{i}. {goal.value}")
    
    while True:
        try:
            choice = int(input("Enter choice (1-3): "))
            if 1 <= choice <= 3:
                health_goal = list(HealthGoal)[choice-1]
                break
            print("Please enter a number between 1 and 3")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    return UserProfile(height, weight, age, gender, health_goal)

def main():
    try:
        user = get_user_input()
        recommendations = user.get_recommendations()
        print("\nYour Health Profile Analysis:")
        print(json.dumps(recommendations, indent=2))
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
