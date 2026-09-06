from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Practitioner
from ..schemas import LoginRequest, PractitionerRes, RefreshRequest, TokenResponse
from ..security import get_current_practitioner
from ..services import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    access_token, refresh_token = AuthService(db).login(payload.email, payload.password)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    access_token, refresh_token = AuthService(db).refresh(payload.refresh_token)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: RefreshRequest, db: Session = Depends(get_db)):
    AuthService(db).logout(payload.refresh_token)


@router.get("/me", response_model=PractitionerRes)
def get_me(current_practitioner: Practitioner = Depends(get_current_practitioner)):
    return current_practitioner
