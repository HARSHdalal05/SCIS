from datetime import date
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SendOtpRequest(BaseModel):
    mobile_number: str = Field(min_length=8, max_length=15)


class SendOtpResponse(BaseModel):
    message: str
    otp_hint: str


class VerifyOtpRequest(BaseModel):
    mobile_number: str
    otp: str


class VerifyOtpResponse(BaseModel):
    token: str
    user_id: int
    is_new_user: bool


class UserCreateRequest(BaseModel):
    mobile_number: str


class UserCreateResponse(BaseModel):
    user_id: int
    message: str


class FitnessProfileRequest(BaseModel):
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    body_fat_percent: Optional[float] = None
    activity_level: str
    fitness_goal: str
    diet_type: str
    whey_protein: bool = False
    workout_days_per_week: int
    training_level: str = "beginner"


class FitnessProfileResponse(FitnessProfileRequest):
    bmi: float
    bmr: float
    daily_calories: float
    macro_protein_g: float
    macro_carbs_g: float
    macro_fats_g: float


class PlanResponse(BaseModel):
    user_id: int
    plan: Dict[str, Any]


class ProgressUpdateRequest(BaseModel):
    user_id: int
    log_date: date
    workout_completed: bool
    calories_consumed: float
    protein_intake_g: float
    weight_kg: Optional[float] = None
    notes: Optional[str] = None


class ProgressUpdateResponse(BaseModel):
    weekly_progress_score: float
    ai_feedback_summary: str


class DashboardResponse(BaseModel):
    user_id: int
    profile: Dict[str, Any]
    latest_workout: Optional[Dict[str, Any]] = None
    latest_diet: Optional[Dict[str, Any]] = None
    progress: Dict[str, Any]
    avatar_state: Dict[str, Any]
    reminders: List[str]
