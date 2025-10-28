
from datetime import datetime
from .models import Reading, Patient
from .repository import ReadingRepo, PatientRepo

class ReadingService:
    def __init__(self, repo: ReadingRepo):
        self.repo = repo

    def validate(self, r: Reading):
        if r.bpsystolic <= 0 or r.bpdiastolic <= 0:
            raise ValueError("Systolic and Diastolic must be greater than 0")
        if r.heartrate <= 0:
            raise ValueError("Heart rate must be greater than 0.")
        if not r.patientcontext.strip():
            raise ValueError("Patient context is required.")

    def list(self, patientid: int | None = None):
        return self.repo.getlist(patientid=patientid)
    
    def search(self, keyword: str):
        return self.repo.search(keyword)


    def create(self, bpsystolic, bpdiastolic, heartrate, patientcontext, timestamp: datetime, notes="", patientid=None):
        r = Reading(None, bpsystolic, bpdiastolic, heartrate, patientcontext, timestamp, notes)
        self.validate(r)
        return self.repo.add(r, patientid=patientid)

    def update(self, r: Reading) -> Reading:
        self.validate(r)
        return self.repo.update(r)

    def delete(self, id_: int) -> None:
        self.repo.delete(id_)


class PatientService:
    def __init__(self, repo: PatientRepo):
        self.repo = repo

    def validate(self, p: Patient):
        if not p.name.strip():
            raise ValueError("Name is required")
        if p.age <= 0:
            raise ValueError("Age must be greater than 0.")
        if p.sex not in ("Male", "Female", "Other"):
            raise ValueError("Invalid sex")

    def list(self):
        return self.repo.list()

    def create(self, name: str, age: int, sex: str, note: str = "") -> Patient:
        p = Patient(None, name, age, sex, note)
        self.validate(p)
        return self.repo.add(p)

    def update(self, p: Patient) -> Patient:
        self.validate(p)
        return self.repo.update(p)

    def delete(self, id_: int) -> None:
        self.repo.delete(id_)
