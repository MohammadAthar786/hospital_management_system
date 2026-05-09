
-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Doctors table
CREATE TABLE doctors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Patients table
CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL CHECK (age > 0 AND age < 150),
    gender VARCHAR(10) CHECK (gender IN ('male', 'female', 'other')),
    blood_pressure NUMERIC(5,2),
    cholesterol NUMERIC(6,2),
    blood_sugar NUMERIC(6,2),
    email VARCHAR(150) UNIQUE,
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Appointments table
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    doctor_id UUID NOT NULL REFERENCES doctors(id) ON DELETE CASCADE,
    appointment_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled'
        CHECK (status IN ('scheduled', 'completed', 'cancelled')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Lab results table
CREATE TABLE lab_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    appointment_id UUID REFERENCES appointments(id),
    test_name VARCHAR(100) NOT NULL,
    result_value NUMERIC(8,2) NOT NULL,
    unit VARCHAR(30),
    normal_min NUMERIC(8,2),
    normal_max NUMERIC(8,2),
    tested_at DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Medications table
CREATE TABLE medications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    drug_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50) NOT NULL,
    frequency VARCHAR(50),
    start_date DATE NOT NULL,
    end_date DATE,
    prescribed_by UUID REFERENCES doctors(id)
);

-- Indexes for fast lookups (this is what you learn in Week 2)
CREATE INDEX idx_patients_name ON patients(name);
CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_lab_results_patient ON lab_results(patient_id);