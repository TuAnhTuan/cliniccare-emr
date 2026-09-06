from datetime import date, datetime, timedelta
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from .base import ORMModel
from .diagnosis import DiagnosisRes
from .patient import PatientRes

# Highest independently verified human age on record is 122 (Jeanne Calment);
# 130 gives a safety margin above that without allowing implausible values.
MAX_PATIENT_AGE_YEARS = 130


class ConsultationCreate(BaseModel):
    patient_name: str = Field(..., min_length=1, max_length=255)
    # Only applied when a new patient is created; ignored for an existing patient match.
    patient_dob: date | None = None
    patient_gender: Literal["male", "female", "other"] | None = None
    note: str = Field(..., min_length=1, max_length=5000)
    diagnosis_codes: list[str] = Field(..., min_length=1)
    # TODO: JWT login is added
    created_by: int

    @field_validator("patient_dob")
    @classmethod
    def validate_patient_dob(cls, value: date | None) -> date | None:
        if value is None:
            return value
        today = date.today()
        if value > today:
            raise ValueError("Date of birth cannot be in the future")
        earliest = today - timedelta(days=MAX_PATIENT_AGE_YEARS * 365.25)
        if value < earliest:
            raise ValueError(f"Date of birth cannot be more than {MAX_PATIENT_AGE_YEARS} years ago")
        return value


class ConsultationRes(ORMModel):
    id: int
    patient: PatientRes
    note: str
    diagnoses: list[DiagnosisRes]
    created_by: int
    created_at: datetime
