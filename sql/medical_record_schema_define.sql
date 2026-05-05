CREATE TABLE medical_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(id),
    appointment_id UUID REFERENCES appointments(id),

    symptoms TEXT,
    diagnosis TEXT,
    risk_level VARCHAR(10),

    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO medical_records (
    id,
    patient_id,
    appointment_id,
    symptoms,
    diagnosis,
    risk_level,
    notes
)
SELECT
    gen_random_uuid(),
    p.id,
    NULL,
    'fever,cough',
    NULL,
    CASE
        WHEN p.blood_sugar > 200 OR p.cholesterol > 250 THEN 'HIGH'
        WHEN p.blood_sugar > 140 OR p.cholesterol > 200 THEN 'MEDIUM'
        ELSE 'LOW'
    END,
    'dummy data for ML dataset pipeline testing'
FROM patients p
WHERE NOT EXISTS (
    SELECT 1
    FROM medical_records mr
    WHERE mr.patient_id = p.id
);

DELETE FROM medical_records
WHERE patient_id IS NULL;

SELECT COUNT(*) 
FROM medical_records 
WHERE patient_id IS NULL;


SELECT conname, pg_get_constraintdef(oid)
FROM pg_constraint
WHERE conrelid = 'patients'::regclass;