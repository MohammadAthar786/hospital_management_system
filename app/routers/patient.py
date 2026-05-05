from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.patient import PatientService
from app.schemas.patients import PatientCreate, PatientUpdate, PatientResponse
from typing import List
from uuid import UUID

router = APIRouter(prefix="/api/v1/patients", tags=["Patients"])

@router.get("/", response_model=List[PatientResponse])
def get_all_patients(db: Session = Depends(get_db)):
    return PatientService(db).get_all_patients()

@router.get("/high-risk", response_model=List[PatientResponse])
def get_high_risk(db: Session = Depends(get_db)):
    return PatientService(db).get_high_risk_patients()

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: UUID, db: Session = Depends(get_db)):
    return PatientService(db).get_patient(patient_id)

@router.post("/", response_model=PatientResponse, status_code=201)
def create_patient(data: PatientCreate, db: Session = Depends(get_db)):
    return PatientService(db).create_patient(data)

@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: UUID, data: PatientUpdate, db: Session = Depends(get_db)):
    return PatientService(db).update_patient(patient_id, data)

@router.delete("/{patient_id}")
def delete_patient(patient_id: UUID, db: Session = Depends(get_db)):
    return PatientService(db).delete_patient(patient_id)