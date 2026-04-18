from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import DietPlan, FitnessProfile, WorkoutPlan
from ..schemas import PlanResponse
from ..services.ai_engine import generate_diet_plan, generate_workout_plan

router = APIRouter(prefix="/generate", tags=["generate"])


@router.post("/workout", response_model=PlanResponse)
def generate_workout(user_id: int = Query(...), db: Session = Depends(get_db)):
    profile = db.query(FitnessProfile).filter(FitnessProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile required")
    plan = generate_workout_plan(profile.fitness_goal, profile.training_level, profile.workout_days_per_week)
    record = WorkoutPlan(user_id=user_id, week_label="week-1", plan_json=plan)
    db.add(record)
    db.commit()
    return PlanResponse(user_id=user_id, plan=plan)


@router.post("/diet", response_model=PlanResponse)
def generate_diet(user_id: int = Query(...), db: Session = Depends(get_db)):
    profile = db.query(FitnessProfile).filter(FitnessProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile required")

    macros = {
        "protein_g": profile.macro_protein_g,
        "carbs_g": profile.macro_carbs_g,
        "fats_g": profile.macro_fats_g,
    }
    plan = generate_diet_plan(profile.daily_calories, macros, profile.diet_type, profile.whey_protein)
    record = DietPlan(user_id=user_id, day_label="day-1", calories=profile.daily_calories, plan_json=plan)
    db.add(record)
    db.commit()
    return PlanResponse(user_id=user_id, plan=plan)
