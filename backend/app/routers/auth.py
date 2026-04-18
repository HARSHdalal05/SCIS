from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import SendOtpRequest, SendOtpResponse, VerifyOtpRequest, VerifyOtpResponse
from ..services.auth import create_token
from ..config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/send-otp", response_model=SendOtpResponse)
def send_otp(payload: SendOtpRequest):
    return SendOtpResponse(message="OTP sent successfully (mock)", otp_hint=f"Use {settings.otp_bypass_code} for MVP")


@router.post("/verify-otp", response_model=VerifyOtpResponse)
def verify_otp(payload: VerifyOtpRequest, db: Session = Depends(get_db)):
    if payload.otp != settings.otp_bypass_code:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    user = db.query(User).filter(User.mobile_number == payload.mobile_number).first()
    is_new = False
    if not user:
        user = User(mobile_number=payload.mobile_number, is_verified=True)
        db.add(user)
        db.commit()
        db.refresh(user)
        is_new = True
    else:
        user.is_verified = True
        db.commit()

    return VerifyOtpResponse(token=create_token(user.id), user_id=user.id, is_new_user=is_new)
