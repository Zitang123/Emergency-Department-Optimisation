import numpy as np

from models.patient import Patient

def generate_one_hour(
        hourly_rate: float,
        acuity_probabilities: list[float],
        mean_treatment_times: dict[int, float],
        seed: int,
) -> list[Patient]:

    if hourly_rate < 0:
        raise ValueError("Hourly rate cannot be negative")

    if len(acuity_probabilities) != 5:
        raise ValueError("Five acuity probabilities required")

    if not np.isclose(sum(acuity_probabilities), 1):
        raise ValueError("Acuity probabilities must sum to 1")

    rng = np.random.default_rng(seed)

    acuity_levels = [1,2,3,4,5]

    number_of_arrivals = int(rng.poisson(lam=hourly_rate))

    patients = []

    for temporary_id in range(1, number_of_arrivals + 1):
        arrival_time = float(rng.uniform(0, 60))

        acuity = int(rng.choice(acuity_levels, p = acuity_probabilities))

        mean_duration = mean_treatment_times[acuity]

        treatment_duration = float(rng.exponential(scale=mean_duration))

        treatment_duration = max(1, treatment_duration)

        patient = Patient(patient_id=temporary_id, arrival_time=arrival_time, acuity=acuity, treatment_duration=treatment_duration)

        patients.append(patient)

    patients.sort(key=lambda patient: patient.arrival_time)

    for final_id, patient in enumerate(patients, start=1):
        patient.patient_id = final_id

    return patients 

def generate_multiple_hours(
        hourly_rates: list[float],
        acuity_probabilities: list[float],
        mean_treatment_times: dict[int, float],
        seed: int,
) -> list[Patient]:

    all_patients = []

    for hour_i, hourly_rate in enumerate(hourly_rates):
        patients_for_this_hour = generate_one_hour(hourly_rate=hourly_rate, acuity_probabilities=acuity_probabilities, mean_treatment_times=mean_treatment_times, seed=seed + hour_i)

        hour_start = hour_i * 60

        for patient in patients_for_this_hour:
            patient.arrival_time += hour_start
            all_patients.append(patient)

    all_patients.sort(key=lambda patient: patient.arrival_time)

    for final_id, patient in enumerate(all_patients, start=1):
        patient.patient_id = final_id

    return all_patients

def estimate_hourly_rate(prior_shape: float,
                         prior_rate: float,
                         observed_counts: list[int],
                         ) -> float:

    if prior_shape <= 0:
        raise ValueError("Prior shape must be positive")

    if prior_rate <= 0:
        raise ValueError("Prior rate must be positive")

    if len(observed_counts) == 0:
        raise ValueError("Observed counts cannot be empty")

    if any(count < 0 for count in observed_counts):
        raise ValueError("Observed counts cannot be negative")

    posterior_shape = prior_shape + sum(observed_counts)

    posterior_rate = prior_rate + len(observed_counts)

    estimated_rate = posterior_shape / posterior_rate

    return estimated_rate
