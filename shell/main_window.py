
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
from datetime import datetime

from features.items.view import VitalTrackerUI
from core.data import get_conn
from features.items.repository import ReadingRepo, PatientRepo
from features.items.service import ReadingService, PatientService


class MainWindow(VitalTrackerUI): #classparent
    def __init__(self):
        super().__init__()

        conn = get_conn() #encap

        self.reading_repo = ReadingRepo(conn)
        self.patient_repo = PatientRepo(conn)

        self.reading_service = ReadingService(self.reading_repo)
        self.patient_service = PatientService(self.patient_repo)

        
        self.connsignals()
        self.recentud()

    def connsignals(self):
        self.addbtn.clicked.connect(self.openread)  #diaforview
        self.rprtbtn.clicked.connect(self.openreadings)
        self.searchbox.textChanged.connect(self.search4patients)

    def openreadings(self):
        readings = self.reading_service.list()
        dialog = reportss(readings, self)
        dialog.exec()

    def search4patients(self):
        keyword = self.searchbox.text().strip()
        self.udlist.clear()

        if not keyword:
            self.recentud()
            return

        results = self.reading_service.search(keyword)
        if not results:
            self.udlist.addItem("No results found.")
        else:
            for r in results:
                ts = r.timestamp
                if isinstance(ts, str):
                    try:
                        ts = datetime.fromisoformat(ts)
                    except:
                        pass
                self.udlist.addItem(
                    f"{r.patientcontext}: {r.bpdisplay} | {r.hrdisplay} | {ts.strftime('%Y-%m-%d %H:%M')}"
                )

    def recentud(self):
        readings = self.reading_service.list()
        self.udlist.clear()

        for r in readings[:5]:
            ts = r.timestamp
            if isinstance(ts, str):
                try:
                    ts = datetime.fromisoformat(ts)
                except:
                    ts = datetime.now()
            self.udlist.addItem(
                f"{r.patientcontext}: {r.bpdisplay} | {r.hrdisplay} | {ts.strftime('%Y-%m-%d %H:%M')}"
            )


class reportss(QDialog):
    def __init__(self, readings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Readings and Reports")
        self.setFixedSize(1000, 500)

        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Name", "Age", "Sex", "Systolic", "Diastolic", "Heart Rate", "Context", "Notes", "Timestamp"
        ])
        self.table.setRowCount(len(readings))

        for row, r in enumerate(readings):
            ts = r.timestamp
            if isinstance(ts, str):
                try:
                    ts = datetime.fromisoformat(ts)
                except:
                    pass

            self.table.setItem(row, 0, QTableWidgetItem(getattr(r, "patient_name", "")))
            self.table.setItem(row, 1, QTableWidgetItem(str(r.patient_age)))
            self.table.setItem(row, 2, QTableWidgetItem(r.patient_sex))
            self.table.setItem(row, 3, QTableWidgetItem(str(r.bpsystolic)))
            self.table.setItem(row, 4, QTableWidgetItem(str(r.bpdiastolic)))
            self.table.setItem(row, 5, QTableWidgetItem(str(r.heartrate)))
            self.table.setItem(row, 6, QTableWidgetItem(r.patientcontext))
            self.table.setItem(row, 7, QTableWidgetItem(r.notes))
            self.table.setItem(row, 8, QTableWidgetItem(ts.strftime("%Y-%m-%d %H:%M")))

        self.table.resizeColumnsToContents()
        layout.addWidget(self.table)
