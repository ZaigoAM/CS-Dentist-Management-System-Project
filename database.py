import mysql.connector
from mysql.connector import Error

DB_HOST, DB_USER, DB_PASSWORD, DB_NAME = "localhost","root","ikigai123","dental_db"

def connection(include_db=True):
    try:
        if include_db:
            connect = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
        else:
            connect = mysql.connector.connect(
                            host=DB_HOST,
                            user=DB_USER,
                            password=DB_PASSWORD
                        )
        return connect
    except Error as e:
        print(f"Error: {e}")
        return None

def init():
    con = connection(include_db=False) #Establishing the connection using previous function
    if con and con.is_connected(): #Creating DB if it doesn't exist
        cursor = con.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        cursor.close()
        con.close()
    con = connection(include_db=True)
    if con and con.is_connected():
        cursor = con.cursor()
        #Creating the two tables 'patients' and 'appointments' if they don't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT NOT NULL,
                gender VARCHAR(10) NOT NULL,
                phone VARCHAR(15) NOT NULL,
                treatment VARCHAR(255) NOT NULL,
                status VARCHAR(20) DEFAULT 'Ongoing'
            );
        """) #Creates the table 'patients'

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INT AUTO_INCREMENT PRIMARY KEY,
                patient_id INT NOT NULL,
                appointment_date DATE NOT NULL,
                time_slot VARCHAR(31) NOT NULL,
                notes TEXT,
                status VARCHAR(31) DEFAULT 'Ongoing',
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
            );
        """)#on delete cascade deletes all appointment related to a patient that is deleted

        con.commit()
        cursor.close()
        con.close()
        print("Database and Tables successfuly initialized.")

def add_patient(name, age, gender, phone, treatment, status = 'Ongoing'): #Add a patient to the database
    con = connection()
    if con and con.is_connected():
        cursor = con.cursor()
        query = """
        INSERT INTO patients (name, age, gender, phone, treatment, status)
        VALUES (%s,%s,%s,%s,%s,%s);
        """
        values = (name,age,gender,phone,treatment,status)
        cursor.execute(query,values)
        con.commit()
        cursor.close()
        con.close()
        return True
    else:
        return False

def delete_patient(patient_id):
    con = connection()
    if con and con.is_connected():
        cursor = con.cursor()
        query = """
        DELETE FROM patients WHERE patient_id = %s;
        """
        cursor.execute(query, (patient_id,))
        con.commit()
        cursor.close()
        con.close()
        return True
    else:
        return False

def fetch_patient(search): #Fetches patients whose name or phone contain whatever you searched
    con = connection()
    if con and con.is_connected():
        cursor = con.cursor()
        if search:
            query = "SELECT * FROM patients WHERE name LIKE %s OR phone LIKE %s ORDER BY patient_id DESC;"
            values = (f"%{search}%", f"%{search}%")
            cursor.execute(query, values)
        else:
            query = "SELECT * FROM patients ORDER BY patient_id DESC;"
            cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        con.close()
        return results

def update_patient(patient_id, name, age, gender, phone, treatment, status): #update a patient's name, age, gender, phone, treatment or status
    con = connection()
    if con and con.is_connected():
        cursor = con.cursor()
        query = """
        UPDATE patients
        SET name=%s, age=%s, gender=%s, phone=%s, treatment=%s, status=%s
        WHERE patient_id=%s;
        """
        values = (name,age,gender,phone,treatment,status,patient_id)
        cursor.execute(query,values)
        con.commit()
        cursor.close()
        con.close()
        return True
    else:
        return False



def add_appointment(patient_id, date, time, notes = "", status = 'Scheduled'): #add an appointment.
    con = connection()
    if con and con.is_connected():
        cursor = con.cursor()
        query = """
        INSERT INTO appointments (patient_id, appointment_date, time_slot, notes, status)
        VALUES (%s,%s,%s,%s,%s);
        """
        values = (patient_id, date, time, notes, status)
        cursor.execute(query, values)
        con.commit()
        cursor.close()
        con.close()
        return True
    else:
        return False

def fetch_appointment(patient_id=None, appointment_date=None, search=""): #fetch an appointment using the patient id, date or a search command
    con = connection()
    appointments = []
    if con and con.is_connected():
        cursor = con.cursor()

        query = """
        SELECT a.appointment_id, p.patient_id, p.name, p.phone, a.appointment_date, a.time_slot, a.notes, a.status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        """
        conditions, parameters = [], []

        if patient_id:
            conditions.append("a.patient_id = %s")
            parameters.append(patient_id)
        if appointment_date:
            conditions.append("a.appointment_date = %s")
            parameters.append(appointment_date)
        if search:
            conditions.append("(p.name LIKE %s OR p.phone LIKE %s)")
            parameters.extend([f"%{search}%", f"%{search}%"])

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY a.appointment_date ASC, a.time_slot ASC;"

        cursor.execute(query, tuple(parameters))
        appointments = cursor.fetchall()
        cursor.close()
        con.close()
    return appointments

def update_appointment(appointment_id,date, time,notes, status): #update an appointment date, time, note or status.
    con = connection()
    if con and con.is_connected():
        cursor = con.cursor()
        query = """
        UPDATE appointments
        SET appointment_date=%s, time_slot=%s,notes=%s, status=%s
        WHERE appointment_id=%s;
        """
        values = (date,time,notes,status,appointment_id)
        cursor.execute(query,values)
        con.commit()
        cursor.close()
        con.close()
        return True
    else:
        return False

def delete_appointment(appointment_id): #Delete an appointment using the id
    con = connection()
    if not con or not con.is_connected():
        return False
    cursor = None
    try:
        cursor = con.cursor()
        query = """
            DELETE FROM appointments
            WHERE appointment_id = %s
        """
        cursor.execute(query, (appointment_id,))
        con.commit()
        return True
    except Error as e:
        con.rollback()
        print(f"Error deleting appointment: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        con.close()

if __name__ == "__main__":
    init()

