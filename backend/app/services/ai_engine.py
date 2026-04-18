from collections import defaultdict
from datetime import date, timedelta
from typing import Dict, List


ACTIVITY_MULTIPLIER = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100
    return round(weight_kg / (height_m * height_m), 2)


def calculate_bmr(gender: str, weight_kg: float, height_cm: float, age: int) -> float:
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    if gender.lower() == "male":
        base += 5
    else:
        base -= 161
    return round(base, 2)


def calculate_calories(bmr: float, activity_level: str, goal: str) -> float:
    calories = bmr * ACTIVITY_MULTIPLIER.get(activity_level.lower(), 1.375)
    goal = goal.lower()
    if goal == "fat loss":
        calories -= 400
    elif goal == "muscle gain":
        calories += 300
    return round(max(calories, 1200), 2)


def calculate_macros(weight_kg: float, calories: float, goal: str) -> Dict[str, float]:
    goal = goal.lower()
    if goal == "muscle gain":
        protein_factor = 2.2
    elif goal == "fat loss":
        protein_factor = 2.0
    else:
        protein_factor = 1.6

    protein = round(weight_kg * protein_factor, 2)
    fat = round(max((calories * 0.25) / 9, weight_kg * 0.6), 2)
    carbs = round(max((calories - (protein * 4 + fat * 9)) / 4, 40), 2)
    return {"protein_g": protein, "carbs_g": carbs, "fats_g": fat}


def generate_workout_plan(goal: str, training_level: str, workout_days: int) -> Dict:
    goal = goal.lower()
    training_level = training_level.lower()
    volume_mult = 0.8 if training_level == "beginner" else 1.0
    sets = int(3 * volume_mult)
    reps = "10-12" if goal != "fat loss" else "12-15"

    if goal == "muscle gain":
        template_days = [
            ("Push", ["Bench Press", "Overhead Press", "Dips", "Lateral Raise"]),
            ("Pull", ["Lat Pulldown", "Seated Row", "Face Pull", "Bicep Curl"]),
            ("Legs", ["Squat", "Romanian Deadlift", "Lunges", "Leg Press"]),
        ]
    else:
        template_days = [
            ("Full Body + Cardio", ["Goblet Squat", "Push-Up", "Row", "Plank", "Treadmill"]),
            ("HIIT + Core", ["Burpees", "Mountain Climbers", "Kettlebell Swing", "Russian Twist"]),
            ("Cardio + Mobility", ["Cycling", "Jogging", "Dynamic Stretch", "Foam Roll"]),
        ]

    plan = {"weekly_plan": []}
    for i in range(max(1, workout_days)):
        title, exercises = template_days[i % len(template_days)]
        day_exercises = [
            {
                "exercise": ex,
                "sets": sets,
                "reps": reps,
                "rest_seconds": 60 if goal == "fat loss" else 90,
            }
            for ex in exercises
        ]
        if training_level != "beginner":
            day_exercises.append(
                {
                    "exercise": "Progressive Overload Marker",
                    "sets": 1,
                    "reps": "Track +2.5% load weekly",
                    "rest_seconds": 0,
                }
            )
        plan["weekly_plan"].append({"day": i + 1, "focus": title, "exercises": day_exercises})
    return plan


def _meal_options(diet_type: str, whey: bool) -> Dict[str, List[str]]:
    veg = {
        "breakfast": ["Oats + milk + nuts", "Paneer bhurji + roti"],
        "lunch": ["Dal + rice + salad", "Chickpea quinoa bowl"],
        "dinner": ["Tofu stir-fry + millet", "Paneer salad bowl"],
        "snacks": ["Fruit + peanut butter", "Greek yogurt"],
    }
    non_veg = {
        "breakfast": ["Egg omelette + toast", "Oats + yogurt"],
        "lunch": ["Chicken breast + rice + veggies", "Fish + sweet potato"],
        "dinner": ["Turkey wrap + salad", "Egg curry + roti"],
        "snacks": ["Fruit + nuts", "Boiled eggs"],
    }
    vegan = {
        "breakfast": ["Soy yogurt parfait", "Overnight oats + chia"],
        "lunch": ["Lentil bowl + quinoa", "Tofu rice bowl"],
        "dinner": ["Tempeh stir-fry", "Bean chili + corn"],
        "snacks": ["Roasted chickpeas", "Fruit smoothie"],
    }
    options = {"veg": veg, "non-veg": non_veg, "vegan": vegan}.get(diet_type.lower(), veg)
    if whey:
        options = dict(options)
        options["snacks"] = options["snacks"] + ["Whey protein shake"]
    return options


def generate_diet_plan(daily_calories: float, macros: Dict[str, float], diet_type: str, whey: bool) -> Dict:
    meal_split = {"breakfast": 0.25, "lunch": 0.3, "dinner": 0.3, "snacks": 0.15}
    options = _meal_options(diet_type, whey)
    meals = {}
    for meal, pct in meal_split.items():
        cal = round(daily_calories * pct, 2)
        meals[meal] = {
            "calories": cal,
            "protein_g": round(macros["protein_g"] * pct, 2),
            "carbs_g": round(macros["carbs_g"] * pct, 2),
            "fats_g": round(macros["fats_g"] * pct, 2),
            "options": options[meal],
        }
    return {"daily_calories": daily_calories, "macro_targets": macros, "meals": meals}


def calculate_consistency_score(logs: List[Dict], profile: Dict) -> float:
    if not logs:
        return 0.0
    goal_cal = profile.get("daily_calories", 2000)
    protein_target = profile.get("macro_protein_g", 100)
    score = 0.0
    for log in logs:
        score += 40 if log.get("workout_completed") else 0
        score += 30 * max(0, 1 - abs(log.get("calories_consumed", 0) - goal_cal) / max(goal_cal, 1))
        score += 30 * min(log.get("protein_intake_g", 0) / max(protein_target, 1), 1)
    return round(min(score / len(logs), 100), 2)


def update_avatar_state(bmi: float, body_fat_percent: float | None, consistency_score: float, prev_visibility: float = 0.3):
    bf = body_fat_percent if body_fat_percent is not None else min(max((bmi - 15) * 1.8, 10), 40)
    target = 0.9 - (bf / 100) + (consistency_score / 300)
    target = max(0.15, min(target, 0.9))
    visibility = round(prev_visibility + (target - prev_visibility) * 0.2, 3)

    groups = {
        "chest": round(visibility, 3),
        "arms": round(max(0.1, visibility - 0.05), 3),
        "abs": round(max(0.05, visibility - 0.1), 3),
        "legs": round(max(0.1, visibility - 0.03), 3),
        "back": round(max(0.1, visibility - 0.04), 3),
    }
    return {
        "muscle_visibility_index": visibility,
        "body_fat_estimate": round(bf, 2),
        "consistency_score": consistency_score,
        "muscle_group_visibility": groups,
    }


def build_progress_summary(logs: List[Dict], profile: Dict) -> Dict:
    consistency = calculate_consistency_score(logs, profile)
    if consistency >= 75:
        feedback = "Great consistency. Keep progressive overload and maintain protein targets."
    elif consistency >= 45:
        feedback = "Good progress, but improve workout adherence and meal consistency."
    else:
        feedback = "Low consistency this week. Focus on completing workouts and protein goals."

    weights = [l.get("weight_kg") for l in logs if l.get("weight_kg") is not None]
    change = round(weights[-1] - weights[0], 2) if len(weights) > 1 else 0.0
    return {
        "weekly_progress_score": consistency,
        "weight_change_kg": change,
        "ai_feedback_summary": feedback,
    }


def reminder_messages(last_log_date: date | None) -> List[str]:
    msgs = ["Workout reminder: Train today based on your weekly split.", "Diet reminder: Hit your calorie and protein target."]
    if last_log_date and (date.today() - last_log_date) >= timedelta(days=1):
        msgs.append("Missed workout alert: You missed yesterday's update. Start with a short session today.")
    return msgs
