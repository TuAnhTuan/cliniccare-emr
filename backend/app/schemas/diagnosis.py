from .base import ORMModel


class DiagnosisRes(ORMModel):
    id: int
    icd10_code: str
    description: str
