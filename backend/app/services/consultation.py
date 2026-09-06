import json
from typing import Any

from sqlalchemy.orm import joinedload, selectinload

from ..exceptions import BadRequestError
from ..models import AuditLog, Consultation, Diagnosis, Patient
from ..schemas import ConsultationCreate
from .base import BaseService


class ConsultationService(BaseService):
    def create(self, data: ConsultationCreate) -> Consultation:
        diagnoses = (
            self.db.query(Diagnosis)
            .filter(Diagnosis.icd10_code.in_(data.diagnosis_codes))
            .all()
        )
        found_codes = {d.icd10_code for d in diagnoses}
        missing_codes = set(data.diagnosis_codes) - found_codes
        if missing_codes:
            raise BadRequestError(f"Unknown diagnosis code(s): {', '.join(sorted(missing_codes))}")

        # Reuse an existing patient with the same name instead of creating a duplicate row.
        patient = (
            self.db.query(Patient)
            .filter(Patient.name.ilike(data.patient_name))
            .first()
        )
        if patient is None:
            patient = Patient(name=data.patient_name)
            self.db.add(patient)
            self.db.flush()

        consultation = Consultation(
            patient_id=patient.id,
            note=data.note,
            created_by=data.created_by,
        )
        consultation.diagnoses = diagnoses
        self.db.add(consultation)
        self.db.flush()

        self.db.add(
            AuditLog(
                table_name="consultations",
                record_id=consultation.id,
                action="CREATE",
                performed_by=data.created_by,
                new_data=json.dumps(
                    {
                        "patient_id": patient.id,
                        "note": data.note,
                        "diagnosis_codes": sorted(found_codes),
                    }
                ),
            )
        )

        self.db.commit()
        self.db.refresh(consultation)
        return consultation

    def get_all(
        self,
        patient: str | None = None,
        diagnosis_code: str | None = None,
    ) -> list[type[Consultation]]:
        query = self.db.query(Consultation).options(
            joinedload(Consultation.patient),
            selectinload(Consultation.diagnoses),
        )
        if patient:
            query = query.join(Consultation.patient).filter(Patient.name.ilike(f"%{patient}%"))
        if diagnosis_code:
            query = query.join(Consultation.diagnoses).filter(Diagnosis.icd10_code == diagnosis_code)
        return (query.order_by(Consultation.created_at.desc())
                .distinct()
                .all())
