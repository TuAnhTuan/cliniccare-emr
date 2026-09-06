from typing import Any

from sqlalchemy import case

from ..models import Diagnosis
from .base import BaseService

MIN_SEARCH_LENGTH = 3


class DiagnosisService(BaseService):
    def search(self, search: str, limit: int) -> list[Diagnosis] | list[Any]:
        query = self.db.query(Diagnosis)
        term = search.strip()

        if not term:
            return query.order_by(Diagnosis.icd10_code.asc()).limit(limit).all()

        if len(term) < MIN_SEARCH_LENGTH:
            return []

        code_match = Diagnosis.icd10_code.ilike(f"{term}%")
        description_match = Diagnosis.description.ilike(f"%{term}%")

        # Code matches ranked before description-only matches.
        rank = case((code_match, 0), else_=1)

        return (
            query.filter(code_match | description_match)
            .order_by(rank, Diagnosis.icd10_code.asc())
            .limit(limit)
            .all()
        )
