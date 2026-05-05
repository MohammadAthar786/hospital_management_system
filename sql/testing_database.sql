-- 1. Basic SELECT — get all patients
SELECT * FROM patients;

-- 2. Filter — patients older than 45
SELECT name, age, blood_pressure
FROM patients
WHERE age > 45;

-- 3. ORDER BY — sort by cholesterol descending
SELECT name, cholesterol
FROM patients
ORDER BY cholesterol DESC;

-- 4. INNER JOIN — appointments with patient AND doctor names
SELECT
    p.name AS patient_name,
    d.name AS doctor_name,
    a.appointment_date,
    a.status
FROM appointments a
INNER JOIN patients p ON a.patient_id = p.id
INNER JOIN doctors d  ON a.doctor_id  = d.id;

-- 5. WHERE + JOIN — only completed appointments
SELECT p.name, d.specialty, a.appointment_date
FROM appointments a
JOIN patients p ON a.patient_id = p.id
JOIN doctors  d ON a.doctor_id  = d.id
WHERE a.status = 'completed';

-- 6. COUNT + GROUP BY — how many patients per doctor
SELECT d.name AS doctor, COUNT(a.id) AS total_appointments
FROM doctors d
LEFT JOIN appointments a ON d.id = a.doctor_id
GROUP BY d.name
ORDER BY total_appointments DESC;

-- 7. AVG — average cholesterol by gender
SELECT gender, ROUND(AVG(cholesterol), 2) AS avg_cholesterol
FROM patients
GROUP BY gender;

-- 8. Subquery — patients with cholesterol above average
SELECT name, cholesterol
FROM patients
WHERE cholesterol > (SELECT AVG(cholesterol) FROM patients);

-- 9. LEFT JOIN — patients who have NO appointments yet
SELECT p.name
FROM patients p
LEFT JOIN appointments a ON p.id = a.patient_id
WHERE a.id IS NULL;

-- 10. Lab results JOIN — get test results with patient names
SELECT
    p.name,
    lr.test_name,
    lr.result_value,
    lr.unit,
    lr.tested_at
FROM lab_results lr
JOIN patients p ON lr.patient_id = p.id
ORDER BY lr.tested_at DESC;

-- 11. HAVING — doctors with more than 2 appointments
SELECT d.name, COUNT(a.id) AS appt_count
FROM doctors d
JOIN appointments a ON d.id = a.doctor_id
GROUP BY d.name
HAVING COUNT(a.id) > 2;

-- 12. High-risk patients — multiple conditions at once
SELECT name, age, blood_pressure, cholesterol, blood_sugar
FROM patients
WHERE blood_pressure > 140
   OR cholesterol > 240
   OR blood_sugar > 126
ORDER BY cholesterol DESC;