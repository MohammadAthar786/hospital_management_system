from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.patients import Patient
from typing import List

class PatientRepository(BaseRepository[Patient]):

    def __init__(self, db: Session):
        super().__init__(Patient, db)  # OOP: calling parent __init__

    # Custom query — only in PatientRepository, not in base
    def get_high_risk(self) -> List[Patient]:
        return self.db.query(Patient).filter(
            (Patient.cholesterol   > 240) |
            (Patient.blood_pressure > 140) |
            (Patient.blood_sugar   > 126)
        ).all()

    def get_by_email(self, email: str):
        return self.db.query(Patient).filter(Patient.email == email).first()