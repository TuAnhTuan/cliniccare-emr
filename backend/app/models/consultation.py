from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base

# Association table for the consultation <-> diagnosis many-to-many relationship.
consultation_diagnoses = Table(
    "consultation_diagnoses",
    Base.metadata,
    Column("consultation_id", Integer, ForeignKey("consultations.id", ondelete="CASCADE"), primary_key=True),
    Column("diagnosis_id", Integer, ForeignKey("diagnoses.id"), primary_key=True),
)


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    note = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("practitioners.id"), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_by = Column(Integer, ForeignKey("practitioners.id"), nullable=True)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)

    patient = relationship("Patient", back_populates="consultations")
    diagnoses = relationship("Diagnosis", secondary=consultation_diagnoses)
    practitioner = relationship("Practitioner", foreign_keys=[created_by])
