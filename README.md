# CS-Dentist-Management-System-Project
A dentist patient and appointment management application that removes the need for paper and pen, and wasting mindpower on thinking about appointments. Built in python, using mysql.connectivity. Change the password and username before use in main.py.

Setup and Installation:
Python 3.13.x
MySQL server
MySQL credentials with database creation permissions

step 1: Clone the repository

step 2: Create a virtual environment
Mac:
    python3 -m venv .venv
    source .venv/bin/activate

Windows:
    python -m venv .venv
    .venv\Scripts\activate
    
activation:
mac: source .venv/bin/activate
windows: .venv\Scripts\activate

step 3: Install dependencies
python -m pip install -r requirements.txt

step 4: Configure the database
Open database.py and edit line 4:
    DB_HOST, DB_USER, DB_PASSWORD, DB_NAME = "localhost", "root", "YOUR_PASSWORD", "dental_db"
Replace YOUR_PASSWORD with your local MySQL root password. Leave DB_NAME as is;
init() creates the database and tables automatically on first run.

step 5: RUN
cd Project
python main.py

you should see "Database and Tables successfully initialized." then the main menu screen.



Troubleshooting:
"No module named 'PyQt5'": the virtual environment is not activated. Run the
  activate command from Step 2 in the same terminal you're using.
"Could not find the Qt platform plugin 'cocoa'": run this before python main.py:
      export QT_QPA_PLATFORM_PLUGIN_PATH=$(python -c 'import PyQt5, os; print(os.path.join(os.path.dirname(PyQt5.__file__), "Qt5", "plugins"))')
"Database Error" on every button: MySQL is not running, or the password in
  database.py is wrong. Confirm MySQL is running and the credentials match.
"ModuleNotFoundError: patients_ui": you ran main.py from the wrong folder.
  cd into Project/ first.



Author:
Adivesh Mishra
Computer Science Project, Class 12
