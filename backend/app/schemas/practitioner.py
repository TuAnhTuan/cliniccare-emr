from .base import ORMModel


class PractitionerRes(ORMModel):
    id: int
    full_name: str
    email: str
    role: str
