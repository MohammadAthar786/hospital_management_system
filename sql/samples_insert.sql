-- ============================================
-- HEALTH RECORD SYSTEM — SEED DATA
-- Run: psql -U postgres -d health_db -f seed.sql
-- ============================================


-- ============================================
-- 1. DOCTORS (8 doctors, different specialties)
-- ============================================
INSERT INTO doctors (name, specialty, email, phone) VALUES
('Dr. Aisha Sharma',    'Cardiology',         'aisha.sharma@hospital.com',   '9876543210'),
('Dr. Rohit Verma',     'Neurology',          'rohit.verma@hospital.com',    '9876543211'),
('Dr. Priya Nair',      'General Medicine',   'priya.nair@hospital.com',     '9876543212'),
('Dr. Sameer Khan',     'Endocrinology',      'sameer.khan@hospital.com',    '9876543213'),
('Dr. Neha Gupta',      'Pulmonology',        'neha.gupta@hospital.com',     '9876543214'),
('Dr. Aryan Mehta',     'Orthopedics',        'aryan.mehta@hospital.com',    '9876543215'),
('Dr. Sunita Rao',      'Gynecology',         'sunita.rao@hospital.com',     '9876543216'),
('Dr. Vivek Tiwari',    'Dermatology',        'vivek.tiwari@hospital.com',   '9876543217');


-- ============================================
-- 2. PATIENTS (15 patients, varied health profiles)
-- ============================================
INSERT INTO patients (name, age, gender, blood_pressure, cholesterol, blood_sugar, email, phone) VALUES
('Ramesh Kumar',        45, 'male',   130.5, 210.0, 105.0, 'ramesh.kumar@gmail.com',    '9811111111'),
('Sunita Devi',         60, 'female', 145.0, 255.0, 132.0, 'sunita.devi@gmail.com',     '9822222222'),
('Arjun Singh',         35, 'male',   118.0, 182.0,  93.0, 'arjun.singh@gmail.com',     '9833333333'),
('Meena Patel',         52, 'female', 140.0, 235.0, 118.0, 'meena.patel@gmail.com',     '9844444444'),
('Vikram Joshi',        58, 'male',   158.0, 278.0, 145.0, 'vikram.joshi@gmail.com',    '9855555555'),
('Kavya Reddy',         28, 'female', 110.0, 168.0,  87.0, 'kavya.reddy@gmail.com',     '9866666666'),
('Deepak Rao',          42, 'male',   126.0, 198.0, 101.0, 'deepak.rao@gmail.com',      '9877777777'),
('Anjali Mishra',       33, 'female', 115.0, 175.0,  90.0, 'anjali.mishra@gmail.com',   '9888888888'),
('Suresh Nair',         65, 'male',   162.0, 290.0, 155.0, 'suresh.nair@gmail.com',     '9899999999'),
('Pooja Iyer',          38, 'female', 122.0, 192.0,  97.0, 'pooja.iyer@gmail.com',      '9810101010'),
('Manoj Yadav',         47, 'male',   135.0, 220.0, 110.0, 'manoj.yadav@gmail.com',     '9821212121'),
('Ritu Agarwal',        55, 'female', 148.0, 262.0, 128.0, 'ritu.agarwal@gmail.com',    '9832323232'),
('Karan Malhotra',      29, 'male',   112.0, 160.0,  85.0, 'karan.malhotra@gmail.com',  '9843434343'),
('Divya Kapoor',        44, 'female', 132.0, 215.0, 108.0, 'divya.kapoor@gmail.com',    '9854545454'),
('Harish Pandey',       70, 'male',   168.0, 305.0, 160.0, 'harish.pandey@gmail.com',   '9865656565');


-- ============================================
-- 3. APPOINTMENTS (20 appointments)
-- We reference doctors and patients by subquery
-- so you don't need to hardcode UUIDs
-- ============================================
INSERT INTO appointments (patient_id, doctor_id, appointment_date, status, notes) VALUES

-- Ramesh Kumar — cardiology checkup
((SELECT id FROM patients WHERE email='ramesh.kumar@gmail.com'),
 (SELECT id FROM doctors  WHERE email='aisha.sharma@hospital.com'),
 '2024-11-05', 'completed', 'Routine cardiac checkup. BP slightly elevated.'),

-- Sunita Devi — general medicine + endocrinology
((SELECT id FROM patients WHERE email='sunita.devi@gmail.com'),
 (SELECT id FROM doctors  WHERE email='priya.nair@hospital.com'),
 '2024-11-08', 'completed', 'Complained of fatigue and dizziness.'),

((SELECT id FROM patients WHERE email='sunita.devi@gmail.com'),
 (SELECT id FROM doctors  WHERE email='sameer.khan@hospital.com'),
 '2024-11-20', 'completed', 'Referred for diabetes management.'),

-- Vikram Joshi — high risk patient, multiple visits
((SELECT id FROM patients WHERE email='vikram.joshi@gmail.com'),
 (SELECT id FROM doctors  WHERE email='aisha.sharma@hospital.com'),
 '2024-10-15', 'completed', 'High BP and cholesterol. Prescribed medication.'),

((SELECT id FROM patients WHERE email='vikram.joshi@gmail.com'),
 (SELECT id FROM doctors  WHERE email='sameer.khan@hospital.com'),
 '2024-11-01', 'completed', 'Blood sugar levels dangerously high.'),

((SELECT id FROM patients WHERE email='vikram.joshi@gmail.com'),
 (SELECT id FROM doctors  WHERE email='aisha.sharma@hospital.com'),
 '2024-12-10', 'scheduled', 'Follow-up after medication change.'),

-- Suresh Nair — elderly, multiple issues
((SELECT id FROM patients WHERE email='suresh.nair@gmail.com'),
 (SELECT id FROM doctors  WHERE email='rohit.verma@hospital.com'),
 '2024-11-12', 'completed', 'Memory lapses. Neurological assessment needed.'),

((SELECT id FROM patients WHERE email='suresh.nair@gmail.com'),
 (SELECT id FROM doctors  WHERE email='aisha.sharma@hospital.com'),
 '2024-11-25', 'completed', 'Cardiac stress test done.'),

-- Harish Pandey — highest risk patient
((SELECT id FROM patients WHERE email='harish.pandey@gmail.com'),
 (SELECT id FROM doctors  WHERE email='aisha.sharma@hospital.com'),
 '2024-10-20', 'completed', 'Severe hypertension. Immediate medication started.'),

((SELECT id FROM patients WHERE email='harish.pandey@gmail.com'),
 (SELECT id FROM doctors  WHERE email='sameer.khan@hospital.com'),
 '2024-11-05', 'completed', 'Diabetes type 2 confirmed.'),

((SELECT id FROM patients WHERE email='harish.pandey@gmail.com'),
 (SELECT id FROM doctors  WHERE email='rohit.verma@hospital.com'),
 '2024-12-01', 'scheduled', 'Neurological follow-up scheduled.'),

-- Younger healthy patients — routine checkups
((SELECT id FROM patients WHERE email='arjun.singh@gmail.com'),
 (SELECT id FROM doctors  WHERE email='priya.nair@hospital.com'),
 '2024-11-18', 'completed', 'Annual health checkup. All normal.'),

((SELECT id FROM patients WHERE email='kavya.reddy@gmail.com'),
 (SELECT id FROM doctors  WHERE email='sunita.rao@hospital.com'),
 '2024-11-22', 'completed', 'Routine gynecology visit.'),

((SELECT id FROM patients WHERE email='karan.malhotra@gmail.com'),
 (SELECT id FROM doctors  WHERE email='aryan.mehta@hospital.com'),
 '2024-11-28', 'completed', 'Knee pain from sports injury.'),

((SELECT id FROM patients WHERE email='anjali.mishra@gmail.com'),
 (SELECT id FROM doctors  WHERE email='vivek.tiwari@hospital.com'),
 '2024-12-02', 'scheduled', 'Skin rash consultation.'),

-- Mid-range risk patients
((SELECT id FROM patients WHERE email='meena.patel@gmail.com'),
 (SELECT id FROM doctors  WHERE email='sameer.khan@hospital.com'),
 '2024-11-10', 'completed', 'Pre-diabetic. Lifestyle changes advised.'),

((SELECT id FROM patients WHERE email='ritu.agarwal@gmail.com'),
 (SELECT id FROM doctors  WHERE email='aisha.sharma@hospital.com'),
 '2024-11-15', 'completed', 'Cholesterol very high. Statin prescribed.'),

((SELECT id FROM patients WHERE email='manoj.yadav@gmail.com'),
 (SELECT id FROM doctors  WHERE email='priya.nair@hospital.com'),
 '2024-12-05', 'scheduled', 'Follow-up for hypertension.'),

((SELECT id FROM patients WHERE email='divya.kapoor@gmail.com'),
 (SELECT id FROM doctors  WHERE email='neha.gupta@hospital.com'),
 '2024-11-30', 'completed', 'Shortness of breath. Pulmonary function test done.'),

((SELECT id FROM patients WHERE email='pooja.iyer@gmail.com'),
 (SELECT id FROM doctors  WHERE email='priya.nair@hospital.com'),
 '2024-12-08', 'scheduled', 'General checkup, first visit.');


-- ============================================
-- 4. LAB RESULTS (25 results across patients)
-- ============================================
INSERT INTO lab_results (patient_id, appointment_id, test_name, result_value, unit, normal_min, normal_max, tested_at) VALUES

-- Ramesh Kumar
((SELECT id FROM patients WHERE email='ramesh.kumar@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Routine cardiac checkup. BP slightly elevated.'),
 'Total Cholesterol', 210.0, 'mg/dL', 0.0, 200.0, '2024-11-05'),

((SELECT id FROM patients WHERE email='ramesh.kumar@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Routine cardiac checkup. BP slightly elevated.'),
 'Blood Glucose Fasting', 105.0, 'mg/dL', 70.0, 100.0, '2024-11-05'),

-- Sunita Devi
((SELECT id FROM patients WHERE email='sunita.devi@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Complained of fatigue and dizziness.'),
 'Hemoglobin', 10.2, 'g/dL', 12.0, 16.0, '2024-11-08'),

((SELECT id FROM patients WHERE email='sunita.devi@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Referred for diabetes management.'),
 'HbA1c', 7.8, '%', 0.0, 5.7, '2024-11-20'),

((SELECT id FROM patients WHERE email='sunita.devi@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Referred for diabetes management.'),
 'Blood Glucose Fasting', 132.0, 'mg/dL', 70.0, 100.0, '2024-11-20'),

-- Vikram Joshi (high risk)
((SELECT id FROM patients WHERE email='vikram.joshi@gmail.com'),
 (SELECT id FROM appointments WHERE notes='High BP and cholesterol. Prescribed medication.'),
 'Total Cholesterol', 278.0, 'mg/dL', 0.0, 200.0, '2024-10-15'),

((SELECT id FROM patients WHERE email='vikram.joshi@gmail.com'),
 (SELECT id FROM appointments WHERE notes='High BP and cholesterol. Prescribed medication.'),
 'LDL Cholesterol', 185.0, 'mg/dL', 0.0, 100.0, '2024-10-15'),

((SELECT id FROM patients WHERE email='vikram.joshi@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Blood sugar levels dangerously high.'),
 'Blood Glucose Fasting', 145.0, 'mg/dL', 70.0, 100.0, '2024-11-01'),

((SELECT id FROM patients WHERE email='vikram.joshi@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Blood sugar levels dangerously high.'),
 'HbA1c', 8.5, '%', 0.0, 5.7, '2024-11-01'),

-- Suresh Nair
((SELECT id FROM patients WHERE email='suresh.nair@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Cardiac stress test done.'),
 'Total Cholesterol', 290.0, 'mg/dL', 0.0, 200.0, '2024-11-25'),

((SELECT id FROM patients WHERE email='suresh.nair@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Cardiac stress test done.'),
 'Triglycerides', 210.0, 'mg/dL', 0.0, 150.0, '2024-11-25'),

-- Harish Pandey (highest risk)
((SELECT id FROM patients WHERE email='harish.pandey@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Severe hypertension. Immediate medication started.'),
 'Total Cholesterol', 305.0, 'mg/dL', 0.0, 200.0, '2024-10-20'),

((SELECT id FROM patients WHERE email='harish.pandey@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Diabetes type 2 confirmed.'),
 'HbA1c', 9.2, '%', 0.0, 5.7, '2024-11-05'),

((SELECT id FROM patients WHERE email='harish.pandey@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Diabetes type 2 confirmed.'),
 'Blood Glucose Fasting', 160.0, 'mg/dL', 70.0, 100.0, '2024-11-05'),

((SELECT id FROM patients WHERE email='harish.pandey@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Diabetes type 2 confirmed.'),
 'Creatinine', 1.9, 'mg/dL', 0.6, 1.2, '2024-11-05'),

-- Meena Patel
((SELECT id FROM patients WHERE email='meena.patel@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Pre-diabetic. Lifestyle changes advised.'),
 'Blood Glucose Fasting', 118.0, 'mg/dL', 70.0, 100.0, '2024-11-10'),

((SELECT id FROM patients WHERE email='meena.patel@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Pre-diabetic. Lifestyle changes advised.'),
 'HbA1c', 6.1, '%', 0.0, 5.7, '2024-11-10'),

-- Ritu Agarwal
((SELECT id FROM patients WHERE email='ritu.agarwal@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Cholesterol very high. Statin prescribed.'),
 'Total Cholesterol', 262.0, 'mg/dL', 0.0, 200.0, '2024-11-15'),

((SELECT id FROM patients WHERE email='ritu.agarwal@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Cholesterol very high. Statin prescribed.'),
 'LDL Cholesterol', 175.0, 'mg/dL', 0.0, 100.0, '2024-11-15'),

-- Healthy patients — normal results
((SELECT id FROM patients WHERE email='arjun.singh@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Annual health checkup. All normal.'),
 'Total Cholesterol', 182.0, 'mg/dL', 0.0, 200.0, '2024-11-18'),

((SELECT id FROM patients WHERE email='arjun.singh@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Annual health checkup. All normal.'),
 'Blood Glucose Fasting', 93.0, 'mg/dL', 70.0, 100.0, '2024-11-18'),

((SELECT id FROM patients WHERE email='kavya.reddy@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Routine gynecology visit.'),
 'Hemoglobin', 13.5, 'g/dL', 12.0, 16.0, '2024-11-22'),

((SELECT id FROM patients WHERE email='divya.kapoor@gmail.com'),
 (SELECT id FROM appointments WHERE notes='Shortness of breath. Pulmonary function test done.'),
 'SpO2', 94.0, '%', 95.0, 100.0, '2024-11-30'),

((SELECT id FROM patients WHERE email='deepak.rao@gmail.com'),
 NULL,
 'Total Cholesterol', 198.0, 'mg/dL', 0.0, 200.0, '2024-10-01'),

((SELECT id FROM patients WHERE email='pooja.iyer@gmail.com'),
 NULL,
 'Blood Glucose Fasting', 97.0, 'mg/dL', 70.0, 100.0, '2024-10-10');


-- ============================================
-- 5. MEDICATIONS (18 prescriptions)
-- ============================================
INSERT INTO medications (patient_id, drug_name, dosage, frequency, start_date, end_date, prescribed_by) VALUES

-- Vikram Joshi — BP + Cholesterol + Sugar
((SELECT id FROM patients WHERE email='vikram.joshi@gmail.com'),
 'Amlodipine', '5mg', 'Once daily', '2024-10-15', NULL,
 (SELECT id FROM doctors WHERE email='aisha.sharma@hospital.com')),

((SELECT id FROM patients WHERE email='vikram.joshi@gmail.com'),
 'Atorvastatin', '20mg', 'Once at night', '2024-10-15', NULL,
 (SELECT id FROM doctors WHERE email='aisha.sharma@hospital.com')),

((SELECT id FROM patients WHERE email='vikram.joshi@gmail.com'),
 'Metformin', '500mg', 'Twice daily', '2024-11-01', NULL,
 (SELECT id FROM doctors WHERE email='sameer.khan@hospital.com')),

-- Harish Pandey — highest risk
((SELECT id FROM patients WHERE email='harish.pandey@gmail.com'),
 'Telmisartan', '40mg', 'Once daily', '2024-10-20', NULL,
 (SELECT id FROM doctors WHERE email='aisha.sharma@hospital.com')),

((SELECT id FROM patients WHERE email='harish.pandey@gmail.com'),
 'Insulin Glargine', '20 units', 'Once at bedtime', '2024-11-05', NULL,
 (SELECT id FROM doctors WHERE email='sameer.khan@hospital.com')),

((SELECT id FROM patients WHERE email='harish.pandey@gmail.com'),
 'Rosuvastatin', '10mg', 'Once at night', '2024-10-20', NULL,
 (SELECT id FROM doctors WHERE email='aisha.sharma@hospital.com')),

-- Suresh Nair
((SELECT id FROM patients WHERE email='suresh.nair@gmail.com'),
 'Aspirin', '75mg', 'Once daily', '2024-11-25', NULL,
 (SELECT id FROM doctors WHERE email='aisha.sharma@hospital.com')),

((SELECT id FROM patients WHERE email='suresh.nair@gmail.com'),
 'Atorvastatin', '40mg', 'Once at night', '2024-11-25', NULL,
 (SELECT id FROM doctors WHERE email='aisha.sharma@hospital.com')),

-- Sunita Devi
((SELECT id FROM patients WHERE email='sunita.devi@gmail.com'),
 'Metformin', '500mg', 'Once daily', '2024-11-20', NULL,
 (SELECT id FROM doctors WHERE email='sameer.khan@hospital.com')),

((SELECT id FROM patients WHERE email='sunita.devi@gmail.com'),
 'Iron Supplement', '150mg', 'Twice daily', '2024-11-08', '2025-02-08',
 (SELECT id FROM doctors WHERE email='priya.nair@hospital.com')),

-- Ritu Agarwal
((SELECT id FROM patients WHERE email='ritu.agarwal@gmail.com'),
 'Atorvastatin', '20mg', 'Once at night', '2024-11-15', NULL,
 (SELECT id FROM doctors WHERE email='aisha.sharma@hospital.com')),

-- Ramesh Kumar
((SELECT id FROM patients WHERE email='ramesh.kumar@gmail.com'),
 'Losartan', '50mg', 'Once daily', '2024-11-05', NULL,
 (SELECT id FROM doctors WHERE email='aisha.sharma@hospital.com')),

-- Meena Patel
((SELECT id FROM patients WHERE email='meena.patel@gmail.com'),
 'Metformin', '250mg', 'Once daily', '2024-11-10', NULL,
 (SELECT id FROM doctors WHERE email='sameer.khan@hospital.com')),

-- Manoj Yadav
((SELECT id FROM patients WHERE email='manoj.yadav@gmail.com'),
 'Amlodipine', '2.5mg', 'Once daily', '2024-11-01', NULL,
 (SELECT id FROM doctors WHERE email='priya.nair@hospital.com')),

-- Karan Malhotra — short course for injury
((SELECT id FROM patients WHERE email='karan.malhotra@gmail.com'),
 'Ibuprofen', '400mg', 'Thrice daily with food', '2024-11-28', '2024-12-05',
 (SELECT id FROM doctors WHERE email='aryan.mehta@hospital.com')),

-- Divya Kapoor
((SELECT id FROM patients WHERE email='divya.kapoor@gmail.com'),
 'Montelukast', '10mg', 'Once at bedtime', '2024-11-30', NULL,
 (SELECT id FROM doctors WHERE email='neha.gupta@hospital.com')),

-- Anjali Mishra — skin treatment
((SELECT id FROM patients WHERE email='anjali.mishra@gmail.com'),
 'Cetirizine', '10mg', 'Once daily', '2024-12-02', '2024-12-16',
 (SELECT id FROM doctors WHERE email='vivek.tiwari@hospital.com')),

-- Deepak Rao — borderline cholesterol watch
((SELECT id FROM patients WHERE email='deepak.rao@gmail.com'),
 'Omega-3 Supplement', '1000mg', 'Once daily', '2024-10-01', NULL,
 (SELECT id FROM doctors WHERE email='priya.nair@hospital.com'));