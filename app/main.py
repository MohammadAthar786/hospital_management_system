from fastapi import FastAPI
from app.routers import patient
from app.routers import doctors
from app.routers import appointments
from app.routers import doctor_leave
app = FastAPI(
    title="Smart Patient Health Record System",
    description="Backend API for managing patient records and disease risk prediction",
    version="1.0.0"
)

app.include_router(patient.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(doctor_leave.router)
@app.get("/")
def root():
    return {"message": "Health Record API is running"}