from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.doctor import Doctor
from typing import List

class DoctorRepository(BaseRepository[Doctor]):
    def __init__(self, db: Session):
        super().__init__(Doctor, db)

    def get_by_email(self, email: str) -> Doctor | None:
        return self.db.query(Doctor).filter(Doctor.email == email).first()

    def get_by_phone(self, phone: str) -> Doctor | None:
        return self.db.query(Doctor).filter(Doctor.phone == phone).first()

    def get_by_specialty(self, specialty: str) -> List[Doctor]:
        return self.db.query(Doctor).filter(Doctor.specialty.ilike(specialty)).all()

    def count_by_specialty(self, specialty: str) -> int:
        return self.db.query(Doctor).filter(Doctor.specialty.ilike(specialty)).count()
  