import os
import random
import uuid
from pathlib import Path
from datetime import date, timedelta

import psycopg2
from faker import Faker
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

fake = Faker("en_IN")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "health_db")
DB_USER = os.getenv("DB_USER", "postgres")

DB_PASSWORD = os.getenv("DB_PASSWORD", "")


def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def calculate_risk(bp, cholesterol, sugar, abnormal_lab_count):
    score = 0

    if bp > 140:
        score += 1
    if cholesterol > 220:
        score += 1
    if sugar > 160:
        score += 1
    if abnormal_lab_count >= 3:
        score += 2
    elif abnormal_lab_count >= 1:
        score += 1

    if score <= 1:
        return "LOW"
    elif score <= 3:
        return "MEDIUM"
    else:
        return "HIGH"


def generate_data(total_patients=300):
    conn = get_conn()
    cur = conn.cursor()

    try:
        doctor_ids = []

        # 1. Doctors
        specialties = ["Cardiology", "General Medicine", "Neurology", "Orthopedics", "Dermatology"]

        for _ in range(10):
            doctor_id = str(uuid.uuid4())
            doctor_ids.append(doctor_id)

            cur.execute(
                """
                INSERT INTO doctors
                (id, name, specialty, email, phone, experience)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    doctor_id,
                    fake.name(),
                    random.choice(specialties),
                    fake.unique.email(),
                    fake.msisdn()[:10],
                    random.randint(1, 25),
                ),
            )

        # 2. Beds
        bed_ids = []

        for i in range(1, 51):
            cur.execute(
                """
                INSERT INTO bed
                (ward, bed_number, bed_type, is_available)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (
                    random.choice(["General", "ICU", "Emergency", "Private"]),
                    f"B-{i}",
                    random.choice(["GENERAL", "ICU", "PRIVATE"]),
                    True,
                ),
            )
            bed_ids.append(cur.fetchone()[0])

        lab_tests = [
            ("Hemoglobin", 12, 17),
            ("WBC Count", 4000, 11000),
            ("Platelet Count", 150000, 450000),
            ("Blood Sugar", 70, 140),
            ("Cholesterol", 120, 200),
            ("Creatinine", 0.6, 1.3),
        ]

        drug_names = ["Paracetamol", "Metformin", "Atorvastatin", "Amlodipine", "Pantoprazole"]
        symptoms_list = [
            "fever,cough",
            "fatigue,headache",
            "chest pain,breathlessness",
            "body pain,weakness",
            "dizziness,nausea",
        ]

        # 3. Patients + linked records
        for _ in range(total_patients):
            patient_id = str(uuid.uuid4())

            age = random.randint(18, 85)
            gender = random.choice(["male", "female", "other"])
            bp = random.randint(95, 180)
            cholesterol = random.randint(130, 300)
            sugar = random.randint(70, 260)

            cur.execute(
                """
                INSERT INTO patients
                (id, name, age, gender, blood_pressure, cholesterol, blood_sugar, email, phone)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    patient_id,
                    fake.name(),
                    age,
                    gender,
                    bp,
                    cholesterol,
                    sugar,
                    fake.unique.email(),
                    fake.msisdn()[:10],
                ),
            )

            # Appointments
            appointment_ids = []
            for _ in range(random.randint(1, 4)):
                appointment_id = str(uuid.uuid4())
                appointment_ids.append(appointment_id)

                cur.execute(
                    """
                    INSERT INTO appointments
                    (id, patient_id, doctor_id, appointment_date, status, notes)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        appointment_id,
                        patient_id,
                        random.choice(doctor_ids),
                        date.today() - timedelta(days=random.randint(1, 365)),
                        random.choice(["completed", "scheduled", "cancelled"]),
                        "dummy appointment",
                    ),
                )

            # Lab results
            abnormal_count = 0
            selected_tests = random.sample(lab_tests, random.randint(3, 6))

            for test_name, normal_min, normal_max in selected_tests:
                if random.random() < 0.3:
                    result_value = random.choice([
                        normal_min - random.uniform(1, 20),
                        normal_max + random.uniform(1, 50),
                    ])
                    abnormal_count += 1
                else:
                    result_value = random.uniform(normal_min, normal_max)

                cur.execute(
                    """
                    INSERT INTO lab_results
                    (id, patient_id, appointment_id, test_name, result_value, unit, normal_min, normal_max, tested_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        str(uuid.uuid4()),
                        patient_id,
                        random.choice(appointment_ids),
                        test_name,
                        round(result_value, 2),
                        "unit",
                        normal_min,
                        normal_max,
                        date.today() - timedelta(days=random.randint(1, 180)),
                    ),
                )

            # Medications
            for _ in range(random.randint(0, 3)):
                start_date = date.today() - timedelta(days=random.randint(1, 90))
                end_date = None if random.random() < 0.5 else start_date + timedelta(days=random.randint(10, 120))

                cur.execute(
                    """
                    INSERT INTO medications
                    (id, patient_id, drug_name, dosage, frequency, start_date, end_date, prescribed_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        str(uuid.uuid4()),
                        patient_id,
                        random.choice(drug_names),
                        random.choice(["250mg", "500mg", "10mg"]),
                        random.choice(["Once daily", "Twice daily", "After meals"]),
                        start_date,
                        end_date,
                        random.choice(doctor_ids),
                    ),
                )

            # Bed allocation for some patients
            if random.random() < 0.25:
                cur.execute(
                    """
                    INSERT INTO bed_allocation
                    (patient_id, bed_id, allocated_at, released_at)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        patient_id,
                        random.choice(bed_ids),
                        fake.date_time_between(start_date="-30d", end_date="now"),
                        None if random.random() < 0.6 else fake.date_time_between(start_date="-10d", end_date="now"),
                    ),
                )

            # Medical record
            risk_level = calculate_risk(bp, cholesterol, sugar, abnormal_count)

            cur.execute(
                """
                INSERT INTO medical_records
                (id, patient_id, appointment_id, symptoms, diagnosis, risk_level, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    str(uuid.uuid4()),
                    patient_id,
                    random.choice(appointment_ids),
                    random.choice(symptoms_list),
                    None,
                    risk_level,
                    "dummy medical record for ML training",
                ),
            )

        conn.commit()
        print(f"Successfully inserted dummy data for {total_patients} patients.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    generate_data(total_patients=300)