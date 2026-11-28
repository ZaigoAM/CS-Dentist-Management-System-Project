import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QGroupBox,
    QLineEdit, QComboBox, QSpinBox, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QTimer
)
from PyQt5.QtCore import Qt
import database

class PatientWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_patient_id = None

        self.search_timer = QTimer(self)
        self.search_timer.setSingleShot(True)
        self.search_timer.setInterval(250)
        self.search_timer.timeout.connect(self.load_patients)

        self.init_ui()
        self.load_patients()



    def init_ui(self):
        main_layout = QHBoxLayout(self)

        form_group = QGroupBox("Patient Details")
        form_layout = QVBoxLayout()
        input_fields_layout = QFormLayout()

        self.name_entry = QLineEdit()

        self.age_spinbox = QSpinBox()
        self.age_spinbox.setRange(0, 120)
        self.age_spinbox.setValue(25)

        self.phone_entry = QLineEdit()
        self.treatment_entry = QLineEdit()

        self.gender_menu = QComboBox()
        self.gender_menu.addItems(["Male", "Female", "Other"])

        self.status_menu = QComboBox()
        self.status_menu.addItems(["Ongoing", "Completed", "Cancelled"])

        input_fields_layout.addRow("Full Name *:", self.name_entry)
        input_fields_layout.addRow("Age:", self.age_spinbox)
        input_fields_layout.addRow("Gender:", self.gender_menu)
        input_fields_layout.addRow("Phone *:", self.phone_entry)
        input_fields_layout.addRow("Treatment:", self.treatment_entry)
        input_fields_layout.addRow("Status:", self.status_menu)

        form_layout.addLayout(input_fields_layout)

        self.btn_add = QPushButton("Add Patient")
        self.btn_update = QPushButton("Update Selected")
        self.btn_delete = QPushButton("Delete Selected")
        self.btn_clear = QPushButton("Clear Form")

        self.btn_add.clicked.connect(self.add_patient)
        self.btn_update.clicked.connect(self.update_patient)
        self.btn_delete.clicked.connect(self.delete_patient)
        self.btn_clear.clicked.connect(self.clear_form)

        form_layout.addWidget(self.btn_add)
        form_layout.addWidget(self.btn_update)
        form_layout.addWidget(self.btn_delete)
        form_layout.addWidget(self.btn_clear)
        form_layout.addStretch()

        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group, 1)

        table_group = QGroupBox("Patient Directory")
        table_layout = QVBoxLayout()

        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Search by name or phone...")
        table_layout.addWidget(self.search_entry)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Gender", "Phone", "Treatment", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self.on_row_select)

        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)
        main_layout.addWidget(table_group, 2)


        self.search_entry.textChanged.connect(self.search_timer.start)

    def load_patients(self):
        search_query = self.search_entry.text().strip()
        patients = database.fetch_patient(search_query)

        self.table.setRowCount(0)
        if not patients:
            return

        for row_idx, record in enumerate(patients):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

    def on_row_select(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            return

        row_idx = self.table.currentRow()
        self.selected_patient_id = int(self.table.item(row_idx, 0).text())

        self.name_entry.setText(self.table.item(row_idx, 1).text())

        try:
            self.age_spinbox.setValue(int(self.table.item(row_idx, 2).text()))
        except (ValueError, AttributeError):
            self.age_spinbox.setValue(0)

        self.gender_menu.setCurrentText(self.table.item(row_idx, 3).text())
        self.phone_entry.setText(self.table.item(row_idx, 4).text())
        self.treatment_entry.setText(self.table.item(row_idx, 5).text())
        self.status_menu.setCurrentText(self.table.item(row_idx, 6).text())

    def validate_inputs(self):
        name = self.name_entry.text().strip()
        phone = self.phone_entry.text().strip()
        if not name or not phone:
            QMessageBox.warning(self, "Validation Error", "Full Name and Phone are required fields.")
            return False
        return True

    def add_patient(self):
        if not self.validate_inputs():
            return

        success = database.add_patient(
            name=self.name_entry.text().strip(),
            age=self.age_spinbox.value(),
            gender=self.gender_menu.currentText(),
            phone=self.phone_entry.text().strip(),
            treatment=self.treatment_entry.text().strip(),
            status=self.status_menu.currentText()
        )

        if success:
            self.clear_form()
            self.load_patients()
            QMessageBox.information(self, "Success", "Patient record created successfully.")
        else:
            QMessageBox.critical(self, "Database Error", "Failed to add patient to MySQL database.")

    def update_patient(self):
        if self.selected_patient_id == None:
            QMessageBox.warning(self, "Selection Error", "Please select a patient from the table to update.")
            return

        if not self.validate_inputs():
            return

        success = database.update_patient(
            patient_id=self.selected_patient_id,
            name=self.name_entry.text().strip(),
            age=self.age_spinbox.value(),
            gender=self.gender_menu.currentText(),
            phone=self.phone_entry.text().strip(),
            treatment=self.treatment_entry.text().strip(),
            status=self.status_menu.currentText()
        )

        if success:
            self.clear_form()
            self.load_patients()
            QMessageBox.information(self, "Success", "Patient record updated successfully.")
        else:
            QMessageBox.critical(self, "Database Error", "Failed to update patient record.")

    def delete_patient(self):
        if self.selected_patient_id == None:
            QMessageBox.warning(self, "Selection Error", "Please select a patient to delete.")
            return

        confirm = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this patient record?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            success = database.delete_patient(self.selected_patient_id)
            if success:
                self.clear_form()
                self.load_patients()
                QMessageBox.information(self, "Success", "Patient record deleted successfully.")
            else:
                QMessageBox.critical(self, "Database Error", "Failed to delete patient record.")

    def clear_form(self):
        self.selected_patient_id = None
        self.name_entry.clear()
        self.age_spinbox.setValue(25)
        self.phone_entry.clear()
        self.treatment_entry.clear()
        self.gender_menu.setCurrentIndex(0)
        self.status_menu.setCurrentIndex(0)
        self.table.clearSelection()


if __name__ == "__main__":
    database.init()
    app = QApplication(sys.argv)
    window = PatientWidget()
    window.setWindowTitle("Patient Management System")
    window.resize(1050, 600)
    window.show()
    sys.exit(app.exec_())
