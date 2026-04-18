from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import AvatarState, DietPlan, FitnessProfile, ProgressLog, WorkoutPlan
from ..schemas import DashboardResponse
from ..services.ai_engine import build_progress_summary, reminder_messages

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/data", response_model=DashboardResponse)
def dashboard_data(user_id: int = Query(...), db: Session = Depends(get_db)):
    profile = db.query(FitnessProfile).filter(FitnessProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile required")

    latest_workout = (
        db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).order_by(WorkoutPlan.created_at.desc()).first()
    )
    latest_diet = db.query(DietPlan).filter(DietPlan.user_id == user_id).order_by(DietPlan.created_at.desc()).first()
    avatar = db.query(AvatarState).filter(AvatarState.user_id == user_id).first()
    logs = db.query(ProgressLog).filter(ProgressLog.user_id == user_id).order_by(ProgressLog.log_date.desc()).limit(7).all()
    logs_data = [
        {
            "workout_completed": l.workout_completed,
            "calories_consumed": l.calories_consumed,
            "protein_intake_g": l.protein_intake_g,
            "weight_kg": l.weight_kg,
        }
        for l in logs
    ]
    summary = build_progress_summary(
        logs_data,
        {"daily_calories": profile.daily_calories, "macro_protein_g": profile.macro_protein_g},
    )

    return DashboardResponse(
        user_id=user_id,
        profile={
            "bmi": profile.bmi,
            "daily_calories": profile.daily_calories,
            "macros": {
                "protein_g": profile.macro_protein_g,
                "carbs_g": profile.macro_carbs_g,
                "fats_g": profile.macro_fats_g,
            },
            "goal": profile.fitness_goal,
        },
        latest_workout=latest_workout.plan_json if latest_workout else None,
        latest_diet=latest_diet.plan_json if latest_diet else None,
        progress=summary,
        avatar_state={
            "muscle_visibility_index": avatar.muscle_visibility_index if avatar else 0.3,
            "body_fat_estimate": avatar.body_fat_estimate if avatar else (profile.body_fat_percent or 25.0),
            "consistency_score": avatar.consistency_score if avatar else 0,
            "muscle_group_visibility": avatar.muscle_group_visibility if avatar else {},
        },
        reminders=reminder_messages(logs[0].log_date if logs else None),
    )
