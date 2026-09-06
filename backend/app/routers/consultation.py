from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Practitioner
from ..schemas import ConsultationCreate, ConsultationRes
from ..security import get_current_practitioner
from ..services import ConsultationService

router = APIRouter(prefix="/consultation", tags=["consultation"])


@router.post("", response_model=ConsultationRes, status_code=status.HTTP_201_CREATED)
def create_consultation(
    payload: ConsultationCreate,
    db: Session = Depends(get_db),
    current_practitioner: Practitioner = Depends(get_current_practitioner),
):
    return ConsultationService(db).create(payload, created_by=current_practitioner.id)


@router.get("", response_model=list[ConsultationRes])
def get_list_consultations(
    patient: str | None = Query(None, description="Filter by patient name"),
    diagnosis_code: str | None = Query(None, description="Filter by ICD-10 code"),
    db: Session = Depends(get_db),
):
    return ConsultationService(db).get_all(patient=patient, diagnosis_code=diagnosis_code)
