import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "health_db")
DB_USER = os.getenv("DB_USER", "postgres")
from urllib.parse import quote_plus
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD", ""))

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

query = """
SELECT
    p.id AS patient_id,
    p.age,
    p.gender,
    p.blood_pressure,
    p.cholesterol,
    p.blood_sugar,

    COALESCE(lab_stats.total_lab_tests, 0) AS total_lab_tests,
    COALESCE(lab_stats.abnormal_lab_count, 0) AS abnormal_lab_count,

    COALESCE(app_stats.total_appointments, 0) AS total_appointments,

    COALESCE(med_stats.active_medications_count, 0) AS active_medications_count,

    CASE
        WHEN ba.patient_id IS NOT NULL THEN 1
        ELSE 0
    END AS is_admitted,

    COALESCE(bed_info.bed_type, 'NONE') AS bed_type,

    mr.symptoms,
    mr.risk_level

FROM patients p

LEFT JOIN (
    SELECT
        patient_id,
        COUNT(*) AS total_lab_tests,
        SUM(
            CASE
                WHEN result_value < normal_min OR result_value > normal_max
                THEN 1 ELSE 0
            END
        ) AS abnormal_lab_count
    FROM lab_results
    GROUP BY patient_id
) lab_stats
ON p.id = lab_stats.patient_id

LEFT JOIN (
    SELECT
        patient_id,
        COUNT(*) AS total_appointments
    FROM appointments
    GROUP BY patient_id
) app_stats
ON p.id = app_stats.patient_id

LEFT JOIN (
    SELECT
        patient_id,
        COUNT(*) AS active_medications_count
    FROM medications
    WHERE end_date IS NULL OR end_date >= CURRENT_DATE
    GROUP BY patient_id
) med_stats
ON p.id = med_stats.patient_id

LEFT JOIN (
    SELECT DISTINCT patient_id
    FROM bed_allocation
    WHERE released_at IS NULL
) ba
ON p.id = ba.patient_id

LEFT JOIN (
    SELECT DISTINCT ON (ba.patient_id)
        ba.patient_id,
        b.bed_type
    FROM bed_allocation ba
    JOIN bed b ON ba.bed_id = b.id
    WHERE ba.released_at IS NULL
    ORDER BY ba.patient_id, ba.allocated_at DESC
) bed_info
ON p.id = bed_info.patient_id

LEFT JOIN (
    SELECT DISTINCT ON (patient_id)
        patient_id,
        symptoms,
        risk_level
    FROM medical_records
    ORDER BY patient_id, created_at DESC
) mr
ON p.id = mr.patient_id

WHERE mr.risk_level IS NOT NULL;
"""

def generate_dataset():
    df = pd.read_sql(query, engine)

    output_path = BASE_DIR / "patient_risk_dataset2.csv"
    df.to_csv(output_path, index=False)

    print("Dataset generated successfully!")
    print("Saved at:", output_path)
    print("Shape:", df.shape)
    print(df.head())

if __name__ == "__main__":
    generate_dataset()