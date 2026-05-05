from datetime import datetime, timedelta, date


def make_naive(t):
    if t is not None and t.tzinfo is not None:
        return t.replace(tzinfo=None)
    return t


def add_minutes(time_value, minutes: int):
    time_value = make_naive(time_value)

    return (
        datetime.combine(date.today(), time_value)
        + timedelta(minutes=minutes)
    ).time()


def minutes_between(start_time, end_time):
    start_time = make_naive(start_time)
    end_time = make_naive(end_time)

    return (
        datetime.combine(date.today(), end_time)
        - datetime.combine(date.today(), start_time)
    ).total_seconds() / 60


def find_available_slot(
    doctors,
    appointments,
    preferred_start_time=None,
    slot_minutes=30
):
    if appointments is None:
        appointments = []

    preferred_start_time = make_naive(preferred_start_time)

    for doctor in doctors:
        doctor_start = make_naive(doctor.available_from)
        doctor_end = make_naive(doctor.available_to)

        if not doctor_start or not doctor_end:
            continue

        doctor_appointments = [
            appt for appt in appointments
            if appt.doctor_id == doctor.id
        ]

        doctor_appointments.sort(key=lambda appt: make_naive(appt.start_time))

        # preferred time logic
        if preferred_start_time:
            preferred_end_time = add_minutes(preferred_start_time, slot_minutes)

            if preferred_start_time >= doctor_start and preferred_end_time <= doctor_end:
                conflict = False

                for appt in doctor_appointments:
                    appt_start = make_naive(appt.start_time)
                    appt_end = make_naive(appt.end_time)

                    if preferred_start_time < appt_end and preferred_end_time > appt_start:
                        conflict = True
                        break

                if not conflict:
                    return {
                        "doctor_id": doctor.id,
                        "start_time": preferred_start_time,
                        "end_time": preferred_end_time
                    }

        # normal first available slot logic
        current_time = doctor_start

        for appt in doctor_appointments:
            appt_start = make_naive(appt.start_time)
            appt_end = make_naive(appt.end_time)

            if minutes_between(current_time, appt_start) >= slot_minutes:
                return {
                    "doctor_id": doctor.id,
                    "start_time": current_time,
                    "end_time": add_minutes(current_time, slot_minutes)
                }

            if appt_end > current_time:
                current_time = appt_end

        # after last appointment
        if minutes_between(current_time, doctor_end) >= slot_minutes:
            return {
                "doctor_id": doctor.id,
                "start_time": current_time,
                "end_time": add_minutes(current_time, slot_minutes)
            }

    return None