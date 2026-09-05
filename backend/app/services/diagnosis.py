from typing import Any

from sqlalchemy import or_

from ..models import Diagnosis
from .base import BaseService


class DiagnosisService(BaseService):
    def search(self, search: str, limit: int) -> list[type[Diagnosis]]:
        query = self.db.query(Diagnosis)
        if search:
            term = f"%{search}%"
            query = query.filter(
                or_(
                    Diagnosis.icd10_code.ilike(term),
                    Diagnosis.description.ilike(term),
                )
            )
        return query.limit(limit).all()
