from sqlalchemy import Column, Integer, String

from .base import Base


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, index=True)
    icd10_code = Column(String(10), nullable=False, unique=True, index=True)
    description = Column(String(500), nullable=False, index=True)
