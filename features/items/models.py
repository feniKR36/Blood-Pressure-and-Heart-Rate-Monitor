from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Reading:
    id: Optional[int]
    bpsystolic: int
    bpdiastolic: int
    heartrate: int
    patientcontext: str
    timestamp: datetime
    notes: str = ""
    patient_name: str = ""  
    patient_age: int = 0    
    patient_sex: str = ""   

    @property
    def bpdisplay(self):
        return f"{self.bpsystolic}/{self.bpdiastolic} mmHg"

    @property
    def hrdisplay(self):
        return f"{self.heartrate} bpm"

@dataclass
class Patient:
    id: int | None
    name: str
    age: int
    sex: str
    note: str = ""

    @property
    def patientname(self) -> str:
        return f"{self.name}, {self.age}"
