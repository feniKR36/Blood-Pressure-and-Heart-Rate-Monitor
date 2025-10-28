from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QListWidget, QFrame, QSizePolicy, QComboBox,
    QFormLayout, QDialog, QMessageBox, QStackedWidget
)
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from PyQt6.QtGui import QFont, QIcon, QPixmap
from datetime import datetime


class addread(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Reading")
        self.setFixedSize(300, 350)
        layout = QFormLayout(self)

        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.sex_input = QComboBox()
        self.sex_input.addItems(["Male", "Female", "Other"])
        self.systolic_input = QLineEdit()
        self.diastolic_input = QLineEdit()
        self.heartrate_input = QLineEdit()
        self.context_input = QLineEdit()
        self.notes_input = QLineEdit()

        layout.addRow("Patient Name:", self.name_input)
        layout.addRow("Age:", self.age_input)
        layout.addRow("Sex:", self.sex_input)
        layout.addRow("Systolic BP:", self.systolic_input)
        layout.addRow("Diastolic BP:", self.diastolic_input)
        layout.addRow("Heart Rate:", self.heartrate_input)
        layout.addRow("Context:", self.context_input)
        layout.addRow("Notes:", self.notes_input)

        btnlayout = QHBoxLayout()
        self.submitbtn = QPushButton("Save")
        self.cancelbtn = QPushButton("Cancel")
        btnlayout.addWidget(self.submitbtn)
        btnlayout.addWidget(self.cancelbtn)
        layout.addRow(btnlayout)

        self.cancelbtn.clicked.connect(self.reject)
        self.submitbtn.clicked.connect(self.accept)

    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "age": self.age_input.text().strip(),
            "sex": self.sex_input.currentText(),
            "bpsystolic": self.systolic_input.text().strip(),
            "bpdiastolic": self.diastolic_input.text().strip(),
            "heartrate": self.heartrate_input.text().strip(),
            "context": self.context_input.text().strip(),
            "notes": self.notes_input.text().strip(),
        }


class VitalTrackerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vital Tracker")
        self.setGeometry(100, 100, 1100, 700)
        self.setWindowIcon(QIcon("D:/app/Untitled33.png"))
        self.ui4dash()

        self.addbtn.clicked.connect(self.openread)

        self.patient_service = None
        self.reading_service = None

    def ui4dash(self):
        mainlayout = QHBoxLayout(self)
        mainlayout.setContentsMargins(0, 0, 0, 0)

        
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(300)
        sidebar = QVBoxLayout(self.sidebar)
        sidebar.setAlignment(Qt.AlignmentFlag.AlignTop)
        sidebar.setContentsMargins(20, 40, 20, 20)

        
        logowidhet = QWidget()
        logolayout = QHBoxLayout(logowidhet)

        pixmap = QPixmap("D:/app/Untitled33.png")
        iconlbl = QLabel()
        if not pixmap.isNull():
            pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            iconlbl.setPixmap(pixmap)

        textlabel = QLabel("Vital Tracker")
        textlabel.setFont(QFont("Arial Rounded MT", 20, QFont.Weight.Bold))

        logolayout.addWidget(iconlbl)
        logolayout.addWidget(textlabel)
        logolayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        sidebar.addWidget(logowidhet)
        sidebar.addSpacing(60)

        self.btndashboard = QPushButton("Dashboard")
        self.btnsettings = QPushButton("Settings")

        for btn in [self.btndashboard, self.btnsettings]:
            btn.setObjectName("sidebarButton")
            btn.setFixedHeight(40)
            sidebar.addWidget(btn)

        mainlayout.addWidget(self.sidebar)

        
        self.stack = QStackedWidget()
        self.stack.setObjectName("mainStack")
        mainlayout.addWidget(self.stack)

        
        self.dashboardpage = QWidget()
        self.dashboardpage.setObjectName("dashboardPage")
        dashboardlayout = QVBoxLayout(self.dashboardpage)
        dashboardlayout.setContentsMargins(20, 20, 20, 20)
        dashboardlayout.setSpacing(10)

        
        topbar = QHBoxLayout()
        self.searchbox = QLineEdit()
        self.searchbox.setPlaceholderText("Search for patients here...")
        self.searchbox.setFixedHeight(35)
        self.systime = QLabel(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.systime.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.systime.setObjectName("systemTime")

        topbar.addWidget(self.searchbox)
        topbar.addWidget(self.systime)
        dashboardlayout.addLayout(topbar)

        
        self.welcomefrm = QFrame()
        self.welcomefrm.setObjectName("welcomeFrame")
        welcomelyt = QVBoxLayout(self.welcomefrm)

        welcomelbl = QLabel("Welcome back,")
        welcomelbl.setFont(QFont("Arial Rounded MT", 20, QFont.Weight.Bold))
        welcomelyt.addWidget(welcomelbl)

        btnlayout = QHBoxLayout()


        self.addbtn = QPushButton("  Add new reading")
        self.addbtn.setObjectName("addNewReading")
        self.addbtn.setIcon(QIcon("D:/app/1000006908.png")) 
        self.addbtn.setIconSize(QtCore.QSize(40, 40))
        self.addbtn.setFont(QFont("Arial Rounded MT", 20, QFont.Weight.Bold))

        self.rprtbtn = QPushButton("  Readings and Reports")
        self.rprtbtn.setObjectName("readingsAndReports")
        self.rprtbtn.setIcon(QIcon("D:/app/1000006907.png")) 
        self.rprtbtn.setIconSize(QtCore.QSize(40, 40))
        self.rprtbtn.setFont(QFont("Arial Rounded MT", 20, QFont.Weight.Bold))
        

        for b in [self.addbtn, self.rprtbtn]:
            b.setFixedSize(400, 200)

        btnlayout.addWidget(self.addbtn)
        btnlayout.addWidget(self.rprtbtn)
        welcomelyt.addLayout(btnlayout)
        dashboardlayout.addWidget(self.welcomefrm)

        
        btmlayout = QHBoxLayout()
        btmlayout.setSpacing(20)

        self.udframe = QFrame()
        self.udframe.setObjectName("updatesFrame")
        updtlayout = QVBoxLayout(self.udframe)
        updtlabel = QLabel("Recent update")
        updtlabel.setFont(QFont("Arial Rounded MT", 16, QFont.Weight.Bold))
        updtlayout.addWidget(updtlabel)

        self.udlist = QListWidget()
        updtlayout.addWidget(self.udlist)
        self.udframe.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        btmlayout.addWidget(self.udframe, 1)

        dashboardlayout.addLayout(btmlayout)

        self.settingspg = QWidget()
        self.settingspg.setObjectName("settingsPage")
        settingslyt = QVBoxLayout(self.settingspg)
        settingslyt.setContentsMargins(20, 20, 20, 20)
        settingslyt.setSpacing(2)  #s small space
        settingslyt.setAlignment(Qt.AlignmentFlag.AlignTop)  

        helpdesk = QLabel("Helpdesk")
        helpdesk.setFont(QFont("Arial Rounded MT", 20, QFont.Weight.Bold))
        settingslyt.addWidget(helpdesk, alignment=Qt.AlignmentFlag.AlignTop)

        helpdeskinfo = QLabel("For concerns, please contact vitaltracker@gmail.com")
        helpdeskinfo.setFont(QFont("Arial", 12))
        settingslyt.addWidget(helpdeskinfo, alignment=Qt.AlignmentFlag.AlignTop)

        self.stack.addWidget(self.dashboardpage)
        self.stack.addWidget(self.settingspg)

        self.btndashboard.clicked.connect(lambda: self.stack.setCurrentWidget(self.dashboardpage))
        self.btnsettings.clicked.connect(lambda: self.stack.setCurrentWidget(self.settingspg))
        self.stack.setCurrentWidget(self.dashboardpage)

    def openread(self):
        dialog = addread()
        if dialog.exec():
            data = dialog.get_data()
            try:
                patient = self.patient_service.create(
                    data["name"],
                    int(data["age"]),
                    data["sex"]
                )

                self.reading_service.create(
                    int(data["bpsystolic"]),
                    int(data["bpdiastolic"]),
                    int(data["heartrate"]),
                    data["context"],
                    datetime.now(),
                    data["notes"],
                    patient.id
                )

                QMessageBox.information(self, "Success", "Reading and patient saved successfully!")

                if hasattr(self, "refresh_recent_updates"):
                    self.refresh_recent_updates()

            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
    