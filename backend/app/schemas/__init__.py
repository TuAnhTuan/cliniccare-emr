from .base import ORMModel
from .consultation import ConsultationCreate, ConsultationRes
from .diagnosis import DiagnosisRes
from .patient import PatientRes

__all__ = [
    "ORMModel",
    "DiagnosisRes",
    "PatientRes",
    "ConsultationCreate",
    "ConsultationRes",
]
