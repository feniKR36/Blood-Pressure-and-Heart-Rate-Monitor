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

        btn_layout = QHBoxLayout()
        self.submit_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(self.submit_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addRow(btn_layout)

        self.cancel_btn.clicked.connect(self.reject)
        self.submit_btn.clicked.connect(self.accept)

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

        self.add_btn.clicked.connect(self.openread)

        self.patient_service = None
        self.reading_service = None

    def ui4dash(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(300)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        sidebar_layout.setContentsMargins(20, 40, 20, 20)

        
        logo_widget = QWidget()
        logo_layout = QHBoxLayout(logo_widget)

        pixmap = QPixmap("D:/app/Untitled33.png")
        icon_label = QLabel()
        if not pixmap.isNull():
            pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            icon_label.setPixmap(pixmap)

        text_label = QLabel("Vital Tracker")
        text_label.setFont(QFont("Arial Rounded MT", 20, QFont.Weight.Bold))

        logo_layout.addWidget(icon_label)
        logo_layout.addWidget(text_label)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        sidebar_layout.addWidget(logo_widget)
        sidebar_layout.addSpacing(60)

        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_settings = QPushButton("Settings")

        for btn in [self.btn_dashboard, self.btn_settings]:
            btn.setObjectName("sidebarButton")
            btn.setFixedHeight(40)
            sidebar_layout.addWidget(btn)

        main_layout.addWidget(self.sidebar)

        
        self.stack = QStackedWidget()
        self.stack.setObjectName("mainStack")
        main_layout.addWidget(self.stack)

        
        self.dashboard_page = QWidget()
        self.dashboard_page.setObjectName("dashboardPage")
        dashboard_layout = QVBoxLayout(self.dashboard_page)
        dashboard_layout.setContentsMargins(20, 20, 20, 20)
        dashboard_layout.setSpacing(10)

        
        top_bar = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search for patients here...")
        self.search_box.setFixedHeight(35)
        self.system_time = QLabel(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.system_time.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.system_time.setObjectName("systemTime")

        top_bar.addWidget(self.search_box)
        top_bar.addWidget(self.system_time)
        dashboard_layout.addLayout(top_bar)

        
        self.welcome_frame = QFrame()
        self.welcome_frame.setObjectName("welcomeFrame")
        welcome_layout = QVBoxLayout(self.welcome_frame)

        welcome_label = QLabel("Welcome back,")
        welcome_label.setFont(QFont("Arial Rounded MT", 20, QFont.Weight.Bold))
        welcome_layout.addWidget(welcome_label)

        btn_layout = QHBoxLayout()


        self.add_btn = QPushButton("  Add new reading")
        self.add_btn.setObjectName("addNewReading")
        self.add_btn.setIcon(QIcon("D:/app/1000006908.png"))  # ← change path to your icon
        self.add_btn.setIconSize(QtCore.QSize(40, 40))
        self.add_btn.setFont(QFont("Arial Rounded MT", 20, QFont.Weight.Bold))

        self.reports_btn = QPushButton("  Readings and Reports")
        self.reports_btn.setObjectName("readingsAndReports")
        self.reports_btn.setIcon(QIcon("D:/app/1000006907.png"))  # ← change path to your icon
        self.reports_btn.setIconSize(QtCore.QSize(40, 40))
        self.reports_btn.setFont(QFont("Arial Rounded MT", 20, QFont.Weight.Bold))

        for b in [self.add_btn, self.reports_btn]:
            b.setFixedSize(400, 200)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.reports_btn)
        welcome_layout.addLayout(btn_layout)
        dashboard_layout.addWidget(self.welcome_frame)

        
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        self.updates_frame = QFrame()
        self.updates_frame.setObjectName("updatesFrame")
        updates_layout = QVBoxLayout(self.updates_frame)
        updates_label = QLabel("Recent update")
        updates_label.setFont(QFont("Arial Rounded MT", 16, QFont.Weight.Bold))
        updates_layout.addWidget(updates_label)

        self.updates_list = QListWidget()
        updates_layout.addWidget(self.updates_list)
        self.updates_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        bottom_layout.addWidget(self.updates_frame, 1)

        dashboard_layout.addLayout(bottom_layout)

        #wala nako na add ang update delete na feature sa ui, mybaddddd
        self.settings_page = QWidget()
        self.settings_page.setObjectName("settingsPage")
        settings_layout = QVBoxLayout(self.settings_page)
        settings_layout.setContentsMargins(20, 20, 20, 20)
        settings_layout.setSpacing(2)  # smaller spacing between labels
        settings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # keep content at the top

        helpdesk_label = QLabel("Helpdesk")
        helpdesk_label.setFont(QFont("Arial Rounded MT", 20, QFont.Weight.Bold))
        settings_layout.addWidget(helpdesk_label, alignment=Qt.AlignmentFlag.AlignTop)

        helpdesk_info = QLabel("For concerns, please contact vitaltracker@gmail.com")
        helpdesk_info.setFont(QFont("Arial", 12))
        settings_layout.addWidget(helpdesk_info, alignment=Qt.AlignmentFlag.AlignTop)

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.settings_page)

        self.btn_dashboard.clicked.connect(lambda: self.stack.setCurrentWidget(self.dashboard_page))
        self.btn_settings.clicked.connect(lambda: self.stack.setCurrentWidget(self.settings_page))
        self.stack.setCurrentWidget(self.dashboard_page)



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
