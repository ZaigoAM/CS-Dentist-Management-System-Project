"source .venv/bin/activate"


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
import database
from patients_ui import PatientWidget
from appointments_ui import AppointmentWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Dental Management System')
        self.resize(400,300)

        layout = QVBoxLayout(self)

        self.btn_patients = QPushButton('Patient Management')
        self.btn_appointments = QPushButton('Appointment Management')

        layout.addWidget(self.btn_patients)
        layout.addWidget(self.btn_appointments)
        self.btn_patients.clicked.connect(self.open_patients)
        self.btn_appointments.clicked.connect(self.open_appointments)

        self.patient_window = None
        self.appointment_window = None

    def open_patients(self):
        self.patient_window = PatientWidget()
        self.patient_window.setWindowTitle('Patient Management System')
        self.patient_window.resize(1050,600)
        self.patient_window.show()

    def open_appointments(self):
        self.appointment_window = AppointmentWidget()
        self.appointment_window.setWindowTitle('Appointment Management System')
        self.appointment_window.resize(1050, 600)
        self.appointment_window.show()

if __name__ == '__main__':
    database.init()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())