from .base import ORMModel


class PatientRes(ORMModel):
    id: int
    name: str
