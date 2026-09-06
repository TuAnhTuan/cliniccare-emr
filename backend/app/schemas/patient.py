from datetime import date

from pydantic import computed_field

from .base import ORMModel


class PatientRes(ORMModel):
    id: int
    name: str
    dob: date | None = None
    gender: str | None = None

    @computed_field
    @property
    def age(self) -> int | None:
        if self.dob is None:
            return None
        today = date.today()
        had_birthday = (today.month, today.day) >= (self.dob.month, self.dob.day)
        return today.year - self.dob.year - (0 if had_birthday else 1)
