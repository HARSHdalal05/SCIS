from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    mobile_number = Column(String(20), unique=True, index=True, nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    fitness_profile = relationship("FitnessProfile", back_populates="user", uselist=False)
    avatar_state = relationship("AvatarState", back_populates="user", uselist=False)


class FitnessProfile(Base):
    __tablename__ = "fitness_profile"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    height_cm = Column(Float, nullable=False)
    weight_kg = Column(Float, nullable=False)
    body_fat_percent = Column(Float)
    activity_level = Column(String(40), nullable=False)
    fitness_goal = Column(String(40), nullable=False)
    diet_type = Column(String(40), nullable=False)
    whey_protein = Column(Boolean, default=False)
    workout_days_per_week = Column(Integer, nullable=False)
    training_level = Column(String(20), default="beginner")
    bmi = Column(Float)
    bmr = Column(Float)
    daily_calories = Column(Float)
    macro_protein_g = Column(Float)
    macro_carbs_g = Column(Float)
    macro_fats_g = Column(Float)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = relationship("User", back_populates="fitness_profile")


class WorkoutPlan(Base):
    __tablename__ = "workout_plan"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    week_label = Column(String(20), default="week-1")
    plan_json = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class DietPlan(Base):
    __tablename__ = "diet_plan"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    day_label = Column(String(20), default="day-1")
    calories = Column(Float, nullable=False)
    plan_json = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ProgressLog(Base):
    __tablename__ = "progress_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    log_date = Column(Date, nullable=False)
    workout_completed = Column(Boolean, default=False)
    calories_consumed = Column(Float, default=0)
    protein_intake_g = Column(Float, default=0)
    weight_kg = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class AvatarState(Base):
    __tablename__ = "avatar_state"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    muscle_visibility_index = Column(Float, default=0.3)
    body_fat_estimate = Column(Float, default=25)
    consistency_score = Column(Float, default=0)
    muscle_group_visibility = Column(JSON, nullable=False, default=lambda: {})
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = relationship("User", back_populates="avatar_state")
