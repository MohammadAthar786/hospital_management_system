from sqlalchemy.orm import Session
from app.repositories.patients import PatientRepository
from app.schemas.patients import PatientCreate, PatientUpdate
from fastapi import HTTPException
## snake case convention is used for method_name 
class PatientService:

    def __init__(self, db: Session):
        self.repo = PatientRepository(db)

    def get_all_patients(self):
        return self.repo.get_all()

    def get_patient(self, patient_id):
        patient = self.repo.get_by_id(patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient

    def create_patient(self, data: PatientCreate):
        # Business rule: no duplicate emails
        existing = self.repo.get_by_email(data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        return self.repo.create(data.model_dump())

    def update_patient(self, patient_id, data: PatientUpdate):
        patient = self.repo.update(patient_id, data.model_dump(exclude_unset=True))
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient

    def delete_patient(self, patient_id):
        deleted = self.repo.delete(patient_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Patient not found")
        return {"message": "Patient deleted successfully"}

    def get_high_risk_patients(self):
        return self.repo.get_high_risk()