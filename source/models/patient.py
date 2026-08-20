from dataclasses import dataclass
from typing import Optional

@dataclass
class Patient:
    patient_id: int
    arrival_time: float
    acuity: int
    treatment_duration: float

    required_doctors: int = 1
    required_nurses: int = 1
    required_beds: int = 1

    treatment_start_time: Optional[float] = None
    treatment_end_time: Optional[float] = None

    def __post_init__(self) -> None:
        if self.arrival_time < 0:
            raise ValueError("Arrival time cannot be negative")

        if self.acuity not in range (1, 6):
            raise ValueError("Acuity must be between 1 and 5")

        if self.treatment_duration <= 0:
            raise ValueError("Treatment duration must be positive")
