from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import ConsultationCreate, ConsultationRes
from ..services import ConsultationService

router = APIRouter(prefix="/consultation", tags=["consultation"])


@router.post("", response_model=ConsultationRes, status_code=status.HTTP_201_CREATED)
def create_consultation(payload: ConsultationCreate, db: Session = Depends(get_db)):
    return ConsultationService(db).create(payload)
