from simulation.patient_generation import generate_multiple_hours


hourly_rates = [
    5.0,
    8.0,
    12.0,
    10.0,
]

acuity_probabilities = [
    0.05,
    0.15,
    0.35,
    0.30,
    0.15,
]

mean_treatment_times = {
    1: 120.0,
    2: 90.0,
    3: 60.0,
    4: 40.0,
    5: 20.0,
}

patients = generate_multiple_hours(
    hourly_rates=hourly_rates,
    acuity_probabilities=acuity_probabilities,
    mean_treatment_times=mean_treatment_times,
    seed=42,
)

print("Total patients:", len(patients))

for patient in patients:
    print(
        "ID:",
        patient.patient_id,
        " Arrival:",
        round(patient.arrival_time, 2),
        " Acuity:",
        patient.acuity,
        " Treatment:",
        round(patient.treatment_duration, 2),
    )