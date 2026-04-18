from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import AvatarState, FitnessProfile, User
from ..schemas import FitnessProfileRequest, FitnessProfileResponse, UserCreateRequest, UserCreateResponse
from ..services.ai_engine import calculate_bmi, calculate_bmr, calculate_calories, calculate_macros, update_avatar_state

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/create", response_model=UserCreateResponse)
def create_user(payload: UserCreateRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.mobile_number == payload.mobile_number).first()
    if existing:
        return UserCreateResponse(user_id=existing.id, message="User already exists")
    user = User(mobile_number=payload.mobile_number, is_verified=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserCreateResponse(user_id=user.id, message="User created")


@router.post("/profile", response_model=FitnessProfileResponse)
def upsert_profile(user_id: int = Query(...), payload: FitnessProfileRequest = None, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    bmi = calculate_bmi(payload.weight_kg, payload.height_cm)
    bmr = calculate_bmr(payload.gender, payload.weight_kg, payload.height_cm, payload.age)
    calories = calculate_calories(bmr, payload.activity_level, payload.fitness_goal)
    macros = calculate_macros(payload.weight_kg, calories, payload.fitness_goal)

    profile = db.query(FitnessProfile).filter(FitnessProfile.user_id == user_id).first()
    if not profile:
        profile = FitnessProfile(user_id=user_id)
        db.add(profile)

    for key, value in payload.model_dump().items():
        setattr(profile, key, value)

    profile.bmi = bmi
    profile.bmr = bmr
    profile.daily_calories = calories
    profile.macro_protein_g = macros["protein_g"]
    profile.macro_carbs_g = macros["carbs_g"]
    profile.macro_fats_g = macros["fats_g"]

    avatar = db.query(AvatarState).filter(AvatarState.user_id == user_id).first()
    avatar_data = update_avatar_state(bmi, payload.body_fat_percent, consistency_score=0.0)
    if not avatar:
        avatar = AvatarState(user_id=user_id, **avatar_data)
        db.add(avatar)
    else:
        for k, v in avatar_data.items():
            setattr(avatar, k, v)

    db.commit()
    return FitnessProfileResponse(**payload.model_dump(), bmi=bmi, bmr=bmr, daily_calories=calories, macro_protein_g=macros["protein_g"], macro_carbs_g=macros["carbs_g"], macro_fats_g=macros["fats_g"])


@router.get("/profile", response_model=FitnessProfileResponse)
def get_profile(user_id: int = Query(...), db: Session = Depends(get_db)):
    profile = db.query(FitnessProfile).filter(FitnessProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return FitnessProfileResponse(
        age=profile.age,
        gender=profile.gender,
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        body_fat_percent=profile.body_fat_percent,
        activity_level=profile.activity_level,
        fitness_goal=profile.fitness_goal,
        diet_type=profile.diet_type,
        whey_protein=profile.whey_protein,
        workout_days_per_week=profile.workout_days_per_week,
        training_level=profile.training_level,
        bmi=profile.bmi,
        bmr=profile.bmr,
        daily_calories=profile.daily_calories,
        macro_protein_g=profile.macro_protein_g,
        macro_carbs_g=profile.macro_carbs_g,
        macro_fats_g=profile.macro_fats_g,
    )
