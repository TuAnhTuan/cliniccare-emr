from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from .base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String(50), nullable=False, index=True)
    record_id = Column(Integer, nullable=False, index=True)
    action = Column(String(10), nullable=False)  # CREATE | UPDATE | DELETE
    performed_by = Column(Integer, ForeignKey("practitioners.id"), nullable=False)
    performed_at = Column(DateTime, nullable=False, server_default=func.now())
    old_data = Column(Text, nullable=True)  # JSON snapshot before the change
    new_data = Column(Text, nullable=True)  # JSON snapshot after the change
