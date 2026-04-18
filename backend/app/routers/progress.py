from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import AvatarState, FitnessProfile, ProgressLog
from ..schemas import ProgressUpdateRequest, ProgressUpdateResponse
from ..services.ai_engine import build_progress_summary, update_avatar_state

router = APIRouter(prefix="/progress", tags=["progress"])


@router.post("/update", response_model=ProgressUpdateResponse)
def update_progress(payload: ProgressUpdateRequest, db: Session = Depends(get_db)):
    profile = db.query(FitnessProfile).filter(FitnessProfile.user_id == payload.user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile required")

    log = ProgressLog(**payload.model_dump())
    db.add(log)
    db.commit()

    week_start = date.today() - timedelta(days=6)
    logs = db.query(ProgressLog).filter(ProgressLog.user_id == payload.user_id, ProgressLog.log_date >= week_start).all()
    logs_data = [
        {
            "workout_completed": l.workout_completed,
            "calories_consumed": l.calories_consumed,
            "protein_intake_g": l.protein_intake_g,
            "weight_kg": l.weight_kg,
        }
        for l in logs
    ]

    profile_data = {
        "daily_calories": profile.daily_calories,
        "macro_protein_g": profile.macro_protein_g,
    }
    summary = build_progress_summary(logs_data, profile_data)

    avatar = db.query(AvatarState).filter(AvatarState.user_id == payload.user_id).first()
    prev_visibility = avatar.muscle_visibility_index if avatar else 0.3
    avatar_data = update_avatar_state(
        bmi=profile.bmi,
        body_fat_percent=profile.body_fat_percent,
        consistency_score=summary["weekly_progress_score"],
        prev_visibility=prev_visibility,
    )
    if not avatar:
        avatar = AvatarState(user_id=payload.user_id, **avatar_data)
        db.add(avatar)
    else:
        for k, v in avatar_data.items():
            setattr(avatar, k, v)
    db.commit()

    return ProgressUpdateResponse(
        weekly_progress_score=summary["weekly_progress_score"],
        ai_feedback_summary=summary["ai_feedback_summary"],
    )
