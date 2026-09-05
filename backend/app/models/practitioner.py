from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from .base import Base


class Practitioner(Base):
    __tablename__ = "practitioners"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    role = Column(String(50), nullable=False, default="doctor")
    hashed_password = Column(String(255), nullable=True)  # nullable until JWT auth is implemented
    created_at = Column(DateTime, nullable=False, server_default=func.now())
