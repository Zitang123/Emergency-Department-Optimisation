from models.patient import Patient

def patient_priority_key(patient: Patient):
    return (patient.acuity, patient.arrival_time, patient.patient_id)


class PatientPriorityQueue:
    def __init__(self):
        self._patients: list[Patient] = []

    def add_patient(self, patient: Patient):
        if not isinstance(patient, Patient):
            raise TypeError("Only Patients can enter the queue")

        self._patients.append(patient)

    def add_patients(self, patients: list[Patient]):
        for patient in patients:
            self.add_patient(patient)

    def view_next_patient(self) -> Patient:
        if self.is_empty():
            return None

        return min(self._patients, key=patient_priority_key)

    def next_patient(self) -> Patient:
        patient = self.view_next_patient()

        if patient is None:
            return None

        self._patients.remove(patient)

        return patient 

    def ordered_patients(self) -> list[Patient]:
        return sorted(self._patients, key=patient_priority_key)

    def is_empty(self):
        return len(self._patients) == 0

    def __len__(self):
        return len(self._patients)