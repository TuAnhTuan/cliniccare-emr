from datetime import datetime

from pydantic import BaseModel, Field

from .base import ORMModel
from .diagnosis import DiagnosisRes
from .patient import PatientRes


class ConsultationCreate(BaseModel):
    patient_name: str = Field(..., min_length=1, max_length=255)
    note: str = Field(..., min_length=1, max_length=5000)
    diagnosis_codes: list[str] = Field(..., min_length=1)
    # TODO: JWT login is added
    created_by: int


class ConsultationRes(ORMModel):
    id: int
    patient: PatientRes
    note: str
    diagnoses: list[DiagnosisRes]
    created_by: int
    created_at: datetime
