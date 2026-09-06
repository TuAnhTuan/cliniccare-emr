from .auth import LoginRequest, RefreshRequest, TokenResponse
from .base import ORMModel
from .consultation import ConsultationCreate, ConsultationRes
from .diagnosis import DiagnosisRes
from .patient import PatientRes
from .practitioner import PractitionerRes

__all__ = [
    "ORMModel",
    "DiagnosisRes",
    "PatientRes",
    "PractitionerRes",
    "ConsultationCreate",
    "ConsultationRes",
    "LoginRequest",
    "RefreshRequest",
    "TokenResponse",
]
