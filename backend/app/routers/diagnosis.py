from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import DiagnosisRes
from ..services import DiagnosisService

router = APIRouter(prefix="/diagnosis", tags=["diagnosis"])


@router.get("", response_model=list[DiagnosisRes])
def search_diagnoses(
    search: str = Query("", description="Search term matched against ICD-10 code or description"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return DiagnosisService(db).search(search, limit)
