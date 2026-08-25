from models.patient import Patient
from simulation.priority_queue import PatientPriorityQueue

class ResourceManager:
    def __init__(self, doctors, nurses, beds):
        if doctors < 0 or nurses < 0 or beds < 0:
            raise ValueError("Resource numbers cannot be negative")

        self.available_doctors = doctors
        self.available_nurses = nurses
        self.available_beds = beds

        self.patients_in_treatment = []

    def resources_available(self, patient: Patient):
        return (
            self.available_doctors >= patient.required_doctors
            and self.available_nurses >= patient.required_nurses
            and self.available_beds >= patient.required_beds
        )

    def allocate_resources(self, patient: Patient, current_time):
        if patient.arrival_time > current_time:
            return False

        if patient in self.patients_in_treatment:
            return False

        if not self.resources_available(patient):
            return False

        self.available_doctors -= patient.required_doctors
        self.available_nurses -= patient.required_nurses
        self.available_beds -= patient.required_beds

        patient.treatment_start_time = current_time
        patient.treatment_end_time = current_time + patient.treatment_duration


        self.patients_in_treatment.append(patient)

        return True

    def allocate_next_patient(self, waiting_queue, current_time):
        patient = waiting_queue.view_next_patient()

        if patient is None:
            return None

        if patient.arrival_time > current_time:
            return None

        if not self.resources_available(patient):
            return None

        patient = waiting_queue.next_patient()

        if self.allocate_resources(patient, current_time):
            return patient

        return None

    def release_finished_patients(self, current_time):
        finished_patients = []

        for patient in self.patients_in_treatment.copy():
            if patient.treatment_end_time <= current_time:
                    self.available_doctors += patient.required_doctors
                    self.available_nurses += patient.required_nurses
                    self.available_beds += patient.required_beds

                    self.patients_in_treatment.remove(patient)
                    finished_patients.append(patient)

        return finished_patients
