
from typing import List #composit
from datetime import datetime
from dataclasses import fields as dataclass_fields
from .models import Reading, Patient

class ReadingRepo:#encap
    def __init__(self, conn):
        self.conn = conn#encapsulation + de behaviour [crud under the class] PEROWALANAADDSAUI TT
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bpsystolic INTEGER NOT NULL,
            bpdiastolic INTEGER NOT NULL,
            heartrate INTEGER NOT NULL,
            patientcontext TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            notes TEXT DEFAULT '',
            patientid INTEGER,
            FOREIGN KEY (patientid) REFERENCES patients (id) ON DELETE CASCADE
        )
        """)

    def timestamp(self, ts):
        if isinstance(ts, str):
            try:
                return datetime.fromisoformat(ts)
            except Exception:
                return datetime.now()
        return ts

    def ROWTOREAD(self, row):
        """
        Convert a DB row (expected to contain columns in this order):
        id, bpsystolic, bpdiastolic, heartrate, patientcontext, timestamp, notes, patient_name, patient_age, patient_sex
        into a Reading instance while only passing keyword args that the Reading dataclass accepts.
        """
        if not row:
            return None

        candidate = {
            "id": row[0],
            "bpsystolic": row[1],
            "bpdiastolic": row[2],
            "heartrate": row[3],
            "patientcontext": row[4],
            "timestamp": self.timestamp(row[5]),
            "notes": row[6],
            "patient_name": row[7] if len(row) > 7 else "",
            "patient_age": row[8] if len(row) > 8 else 0,
            "patient_sex": row[9] if len(row) > 9 else "",
        }

       
        reading_field_names = {f.name for f in dataclass_fields(Reading)}
        filtered = {k: v for k, v in candidate.items() if k in reading_field_names}

        return Reading(**filtered)

    def getlist(self, patientid: int | None = None) -> List[Reading]:
        if patientid is not None:
            rows = self.conn.execute(
                """
                SELECT r.id, r.bpsystolic, r.bpdiastolic, r.heartrate,
                       r.patientcontext, r.timestamp, r.notes,
                       COALESCE(p.name, ''), COALESCE(p.age, 0), COALESCE(p.sex, '')
                FROM readings r
                LEFT JOIN patients p ON r.patientid = p.id
                WHERE r.patientid=?
                ORDER BY r.id DESC
                """,
                (patientid,),
            ).fetchall()
        else:
            rows = self.conn.execute(
                """
                SELECT r.id, r.bpsystolic, r.bpdiastolic, r.heartrate,
                       r.patientcontext, r.timestamp, r.notes,
                       COALESCE(p.name, ''), COALESCE(p.age, 0), COALESCE(p.sex, '')
                FROM readings r
                LEFT JOIN patients p ON r.patientid = p.id
                ORDER BY r.id DESC
                """
            ).fetchall()

        return [self.ROWTOREAD(r) for r in rows] if rows else []

    def get(self, id_: int) -> Reading | None:
        row = self.conn.execute(
            """
            SELECT r.id, r.bpsystolic, r.bpdiastolic, r.heartrate,
                   r.patientcontext, r.timestamp, r.notes,
                   COALESCE(p.name, ''), COALESCE(p.age, 0), COALESCE(p.sex, '')
            FROM readings r
            LEFT JOIN patients p ON r.patientid = p.id
            WHERE r.id=?
            """,
            (id_,),
        ).fetchone()

        return self.ROWTOREAD(row) if row else None

    def search(self, keyword: str) -> List[Reading]:
        rows = self.conn.execute(
            """
            SELECT r.id, r.bpsystolic, r.bpdiastolic, r.heartrate,
                   r.patientcontext, r.timestamp, r.notes,
                   COALESCE(p.name, ''), COALESCE(p.age, 0), COALESCE(p.sex, '')
            FROM readings r
            LEFT JOIN patients p ON r.patientid = p.id
            WHERE r.patientcontext LIKE ? OR r.notes LIKE ? OR p.name LIKE ?
            ORDER BY r.id DESC
            """,
            (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
        ).fetchall()

        return [self.ROWTOREAD(r) for r in rows] if rows else []

    def add(self, r: Reading, patientid: int | None = None) -> Reading:
        cur = self.conn.execute(
            """
            INSERT INTO readings (bpsystolic, bpdiastolic, heartrate, patientcontext, timestamp, notes, patientid)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (r.bpsystolic, r.bpdiastolic, r.heartrate, r.patientcontext, r.timestamp.isoformat(), r.notes, patientid),
        )
        self.conn.commit()

     
        insertedrow = (
            cur.lastrowid,
            r.bpsystolic, r.bpdiastolic, r.heartrate,
            r.patientcontext, r.timestamp.isoformat(), r.notes,
            "", 0, ""
        )
        reading = self.ROWTOREAD(insertedrow)
        return reading

    def update(self, r: Reading) -> Reading:
        assert r.id is not None
        self.conn.execute(
            "UPDATE readings SET bpsystolic=?, bpdiastolic=?, heartrate=?, patientcontext=?, timestamp=?, notes=? WHERE id=?",
            (r.bpsystolic, r.bpdiastolic, r.heartrate, r.patientcontext, r.timestamp.isoformat(), r.notes, r.id),
        )
        self.conn.commit()
        return r

    def delete(self, id_: int) -> None:
        self.conn.execute("DELETE FROM readings WHERE id=?", (id_,))
        self.conn.commit()


class PatientRepo:
    def __init__(self, conn):
        self.conn = conn
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            sex TEXT NOT NULL,
            note TEXT DEFAULT ''
        )
        """)

    def list(self) -> List[Patient]:
        rows = self.conn.execute(
            "SELECT id, name, age, sex, note FROM patients ORDER BY id DESC"
        ).fetchall()
        return [Patient(*r) for r in rows] if rows else []

    def get(self, id_: int) -> Patient | None:
        row = self.conn.execute(
            "SELECT id, name, age, sex, note FROM patients WHERE id=?",
            (id_,)
        ).fetchone()
        return Patient(*row) if row else None

    def add(self, p: Patient) -> Patient:
        cur = self.conn.execute(
            "INSERT INTO patients (name, age, sex, note) VALUES (?, ?, ?, ?)",
            (p.name, p.age, p.sex, p.note),
        )
        self.conn.commit()
        return Patient(cur.lastrowid, p.name, p.age, p.sex, p.note)

    def update(self, p: Patient) -> Patient:
        assert p.id is not None
        self.conn.execute(
            "UPDATE patients SET name=?, age=?, sex=?, note=? WHERE id=?",
            (p.name, p.age, p.sex, p.note, p.id),
        )
        self.conn.commit()
        return p

    def delete(self, id_: int) -> None:
        self.conn.execute("DELETE FROM patients WHERE id=?", (id_,))
        self.conn.commit()

