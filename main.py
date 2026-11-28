import sys
from datetime import date, timedelta
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
import database

class AppointmentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_appointment_id = None
        self.selected_appointment = None
        self.init_ui()
        self.load_today()
    def init_ui(self):
        mainlayout = QHBoxLayout(self)
        #Left panels
        leftpanel = QGroupBox("Search|Filters")
        leftlayout = QVBoxLayout()
        #Right return
        rightlayout = QVBoxLayout()
        #Searching now
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText('Search by name or phone')
        #Defining a button to start searches
        self.btn_search = QPushButton('Search')
        self.btn_search.clicked.connect(self.search_appointments)

        leftlayout.addWidget(QLabel('Search for Patient'))
        leftlayout.addWidget(self.search_entry)
        leftlayout.addWidget(self.btn_search)
        leftlayout.addWidget(QLabel('Dates'))
        #Quick dates like today, tomorrow and day after tomorrow searches
        self.btn_today = QPushButton('Today')
        self.btn_today.clicked.connect(self.load_today)
        self.btn_tomorrow = QPushButton('Tomorrow')
        self.btn_tomorrow.clicked.connect(self.load_tomorrow)
        self.btn_dayafter = QPushButton('Day After Tomorrow')
        self.btn_dayafter.clicked.connect(self.load_dayafter)
        leftlayout.addWidget(self.btn_today)
        leftlayout.addWidget(self.btn_tomorrow)
        leftlayout.addWidget(self.btn_dayafter)
        #Specific Date search
        leftlayout.addWidget(QLabel('Specific Date Search'))
        self.datepick = QDateEdit()
        self.datepick.setCalendarPopup(True)
        self.datepick.setDate(QDate.currentDate())
        self.btn_date = QPushButton('Load Selected Date')
        self.btn_date.clicked.connect(self.load_date)

        leftlayout.addWidget(self.datepick)
        leftlayout.addWidget(self.btn_date)
        #Show all appointments, so yo ucan see what's happening
        self.btn_all = QPushButton('Show All Appointments')
        self.btn_all.clicked.connect(self.load_all)
        leftlayout.addWidget(self.btn_all)
        #Culmination of everything we have done for left side, added to a smaller share of the screen
        leftpanel.setLayout(leftlayout)
        mainlayout.addWidget(leftpanel, 1)
        #Now the right side: Appointment table first
        tablegroup = QGroupBox('Appointment Results')
        tablelayout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            'ID',
            'Patient ID',
            'Patient name',
            'Phone',
            'Date',
            'Time',
            'Notes',
            'Status'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#Stretch to fit
        self.table.setSelectionBehavior(QTableWidget.SelectRows)#Rows can be selected
        self.table.setSelectionMode(QTableWidget.SingleSelection)#Only 1 row can be selected
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)#No editing the table
        self.table.itemSelectionChanged.connect(self.on_appointment_select)#Displays at the bottom
        tablelayout.addWidget(self.table)
        tablegroup.setLayout(tablelayout)
        rightlayout.addWidget(tablegroup,2)#The upper right table is now done.
        #Right bottom panel
        detailgroup = QGroupBox('Selected Appointments')
        detaillayout = QFormLayout()
        #All the useful details that we can have are displayed
        self.detailpatient = QLabel("-")
        self.detailphone = QLabel("-")
        self.detaildate = QLabel("-")
        self.detailtime = QLabel("-")
        self.detailnotes = QLabel("-")
        self.detailstatus = QLabel("-")
        #Now the layout
        detaillayout.addRow('patient', self.detailpatient)
        detaillayout.addRow('phone', self.detailphone)
        detaillayout.addRow('date',self.detaildate)
        detaillayout.addRow('time', self.detailtime)
        detaillayout.addRow('notes', self.detailnotes)
        detaillayout.addRow('status', self.detailstatus)
        #Now to change appointment and stuff
        self.btn_edit = QPushButton('Edit Appointment')
        self.btn_edit.clicked.connect(self.edit_appointment)
        self.btn_complete = QPushButton('Complete Appointment')
        self.btn_complete.clicked.connect(self.complete_appointment)
        self.btn_cancel = QPushButton('Cancel Appointment')
        self.btn_cancel.clicked.connect(self.cancel_appointment)
        self.btn_delete = QPushButton('Delete Appointment')
        self.btn_delete.clicked.connect(self.delete_appointment)
        detaillayout.addRow(self.btn_edit, self.btn_complete)
        detaillayout.addRow(self.btn_cancel, self.btn_delete)
        detailgroup.setLayout(detaillayout)
        rightlayout.addWidget(detailgroup,1)
        mainlayout.addLayout(rightlayout,2)
        #The main GUI is done. Now the functions are left

    def load_appointments(self,patient_id=None,appointment_date=None,search=''): #Required for other functions
        appointments = database.fetch_appointment(patient_id=patient_id,appointment_date=appointment_date,search=search)
        self.table.setRowCount(0)
        for row,record in enumerate(appointments):
            self.table.insertRow(row)
            for column,val in enumerate(record):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row,column,item)
    #Functions that are needed for specific dates and easy dates
    def load_today(self):
        self.load_appointments(appointment_date=date.today())
    def load_tomorrow(self):
        self.load_appointments(appointment_date = date.today() + timedelta(days=1))
    def load_dayafter(self):
        self.load_appointments(appointment_date = date.today() + timedelta(days=2))
    def load_date(self):
        selected = self.datepick.date()
        thedate = selected.toPyDate()
        self.load_appointments(appointment_date = thedate)
    #no need to put anything, database.py already does it
    def load_all(self):
        self.load_appointments()

    def search_appointments(self):
        search = self.search_entry.text().strip()
        self.load_appointments(search=search)

    def on_appointment_select(self):
        selected = self.table.selectedItems()
        if not selected:
            return
        
        row = self.table.currentRow()
        self.selected_appointment_id = int(self.table.item(row,0).text())
        self.selected_appointment = {                       # <-- NEW
            "date" : self.table.item(row, 4).text(),
            "time" : self.table.item(row, 5).text(),
            "notes" : self.table.item(row, 6).text(),
            "status" : self.table.item(row, 7).text(),
        }
        self.detailpatient.setText(self.table.item(row,2).text())
        self.detailphone.setText(self.table.item(row,3).text())
        self.detaildate.setText(self.table.item(row,4).text())
        self.detailtime.setText(self.table.item(row,5).text())
        self.detailnotes.setText(self.table.item(row,6).text())
        self.detailstatus.setText(self.table.item(row,7).text())
        #This is all 8 rows of the table.

    def delete_appointment(self):
        if self.selected_appointment_id is None:
            QMessageBox.warning(self,'Selection Error','Please select an appointment')
            return
        confirm = QMessageBox.question(self,'Confirm Delete','Are you sure you want to delete this appointment?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm != QMessageBox.Yes:
            return
        success = database.delete_appointment(self.selected_appointment_id)
        if success:
            self.selected_appointment_id = None
            self.load_appointments()
            QMessageBox.information(self,'Success','Appointment deleted successfully')
        else:
            QMessageBox.critical(self,'Error','Failed to delete appointment')


    def edit_appointment(self):
        if self.selected_appointment_id is None:
            QMessageBox.warning(self,'Selection Error','Please select an appointment')
            return
        dialog = QDialog(self)
        dialog.setWindowTitle('Edit Appointment')
        layout = QFormLayout(dialog)
        newdate = QDateEdit()
        newdate.setCalendarPopup(True)
        newdate.setDate(QDate.fromString(date, "yyyy-MM-dd"))
        newtime = QLineEdit()
        newnote = QTextEdit()
        newstatus = QComboBox()
        newstatus.addItems([
            'Scheduled',
            'Completed',
            'Cancelled',
        ])
        layout.addRow('Date:', newdate)
        layout.addRow('Time:', newtime)
        layout.addRow('Note:', newnote)
        layout.addRow('Status:',newstatus)

        appt = self.selected_appointment
        newdate.setDate(QDate.fromString(appt["date"], "yyyy-MM-dd"))
        newtime.setText(appt["time"])
        newnote.setPlainText(appt["notes"])
        newstatus.setCurrentText(appt["status"])

        btn_save = QPushButton('Save')
        btn_cancel = QPushButton('Cancel')
        layout.addRow(btn_save, btn_cancel)
        btn_cancel.clicked.connect(dialog.reject)

        def save_changes():
            new_date = newdate.date().toPyDate()
            new_time = newtime.text().strip()
            new_notes = newnote.toPlainText().strip()
            new_status = newstatus.currentText()

            success = database.update_appointment(
                self.selected_appointment_id,
                new_date,
                new_time,
                new_notes,
                new_status
            )
            if success:
                dialog.accept()
                self.load_appointments()
                QMessageBox.information(self, 'Success', 'Appointment updated successfully')

            else:
                QMessageBox.critical(self, 'Error', 'Failed to update appointment')
        btn_save.clicked.connect(save_changes)
        dialog.exec_()

    def complete_appointment(self):
        if self.selected_appointment_id == None:
            QMessageBox.warning(self, 'Selection Error', 'Please select an appointment')
            return

        row_data = self.selected_appointment

        success = database.update_appointment(
            self.selected_appointment_id,
            row_data["date"],
            row_data["time"],
            row_data["notes"],
            'Completed'
        )
        if success:
            self.selected_appointment_id = None
            self.selected_appointment = None
            self.load_appointments()
            QMessageBox.information(self, 'Success', 'Appointment completed')
        else:
            QMessageBox.critical(self, 'Error', 'Failed to complete appointment')

    def cancel_appointment(self):
        if self.selected_appointment_id == None:
            QMessageBox.warning(self, 'Selection Error', 'Please select an appointment')
            return
        row_data = self.selected_appointment

        success = database.update_appointment(
            self.selected_appointment_id,
            row_data["date"],
            row_data["time"],
            row_data["notes"],
            'Cancelled'
        )
        if success:
            self.selected_appointment_id = None
            self.selected_appointment = None
            self.load_appointments()
            QMessageBox.information(self, 'Success', 'Appointment cancelled')
        else:
            QMessageBox.critical(self, 'Error', 'Failed to cancel appointment')        
if __name__ == '__main__':
    database.init()
    app = QApplication(sys.argv)
    window = AppointmentWidget()
    window.setWindowTitle("Appointment Management System")
    window.resize(1050, 600)
    window.show()
    sys.exit(app.exec_()) 
