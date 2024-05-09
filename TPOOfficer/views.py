from django.shortcuts import render                     # To Render html files
from django.contrib import messages                     # Showing Error Messages
from django.db import connection                        # Default Database Handler of Django
import pandas as pd                                     # To manage large data from xlsx file
import mysql.connector                                  # Database Hnadler for MySQL
from django.core.files.storage import FileSystemStorage # Save xlsx file on server side (Laptop)

# On clicking "Login" on admin_login.html
def admin_login(request):
    if request.method == 'POST':                        # Form Submitted
        username = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM admin_data WHERE Name = %s AND Password = %s", [username, password])      # Calling Database values
            user = cursor.fetchone()

        if user:                                        # Authentication Success, user exixts
            return render(request, 'admin_index.html')  # Render admin index page
        else:                                           # Authentication failed
            messages.error(request, 'Invalid username or password')

    return render(request, 'admin_login.html')  # First call to admin_login.html


# On pressing the "Import Data" button, after uploading the file
def import_facultyCo_data(request):
    uploaded_file = request.FILES['file']
    fs = FileSystemStorage()

    filename = 'FacultyCoData.xlsx'           # File from user saved as FacultyCoData.xlsx
    fs.save(filename, uploaded_file)
    file_path = fs.path(filename)
    
    df = pd.read_excel('FacultyCoData.xlsx')  # Read Excel file into a Pandas DataFrame

    dataBase = mysql.connector.connect(     # Connect to MySQL Database
        host='localhost',
        user='root',
        passwd='TIGER',
        database='placementcelldb'
    )

    cursorObject = dataBase.cursor()        # Object of Cursor

    # deletes table / previous data if exist
    drop_table = 'DROP TABLE IF EXISTS FacultyCo_Data'
    cursorObject.execute(drop_table)

    # Create Table (If already haven't)
    # table_creation_query = 'CREATE TABLE IF NOT EXISTS Student_Data (Enrollment_No varchar(11), Name varchar(255), Gender varchar(6), Mobile_No varchar(10), Email_Address varchar(25), Aadhar_Card varchar(10), Branch varchar(25), Semester varchar(2))'
    table_creation_query = 'CREATE TABLE IF NOT EXISTS FacultyCo_Data (Employee_Id varchar(6), Password varchar(7))'
    cursorObject.execute(table_creation_query)
    
    # Insert Data into Table query
    query = 'INSERT INTO FacultyCo_Data (Employee_Id, Password) VALUES (%s, %s)'

    # Iterate through DataFrame and execute INSERT query for each row
    for row in df.itertuples():
        cursorObject.execute(query, (row.Employee_Id, row.Password))

    # Commit Changes to the Database
    dataBase.commit()

    # Close Cursor and Database Connection
    cursorObject.close()
    dataBase.close()

    return render(request, 'admin_index.html')      # Redirect back to admin_index.html


def import_studentCo_data(request):
    uploaded_file = request.FILES['file']
    fs = FileSystemStorage()

    filename = 'StudentCoData.xlsx'           # File from user saved as StudentData.xlsx
    fs.save(filename, uploaded_file)
    file_path = fs.path(filename)
    
    df = pd.read_excel('StudentCoData.xlsx')  # Read Excel file into a Pandas DataFrame

    dataBase = mysql.connector.connect(     # Connect to MySQL Database
        host='localhost',
        user='root',
        passwd='TIGER',
        database='placementcelldb'
    )

    cursorObject = dataBase.cursor()        # Object of Cursor

    # deletes table / previous data if exist
    drop_table = 'DROP TABLE IF EXISTS StudentCo_Data'
    cursorObject.execute(drop_table)

    # Create Table (If already haven't)
    #table_creation_query = 'CREATE TABLE IF NOT EXISTS Student_Data (Enrollment_No varchar(11), Name varchar(255), Gender varchar(6), Mobile_No varchar(10), Email_Address varchar(25), Aadhar_Card varchar(10), Branch varchar(25), Semester varchar(2))'
    table_creation_query = 'CREATE TABLE IF NOT EXISTS StudentCo_Data (Enrollment_No varchar(11), Password varchar(7))'
    cursorObject.execute(table_creation_query)
    
    # Insert Data into Table query
    query = 'INSERT INTO StudentCo_Data (Enrollment_No, Password) VALUES (%s, %s)'

    # Iterate through DataFrame and execute INSERT query for each row
    for row in df.itertuples():
        cursorObject.execute(query, (row.Enrollment_No, row.Password))

    # Commit Changes to the Database
    dataBase.commit()

    # Close Cursor and Database Connection
    cursorObject.close()
    dataBase.close()

    return render(request, 'admin_index.html')      # Redirect back to admin_index.html


def addadmin(request):
    return render (request, 'addadmin.html')


# On submitting form of adding admin
def add_admin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    dataBase = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='TIGER',
        database='placementcelldb'
    )

    cursorObject = dataBase.cursor()

    # Insert Admin Data into Table query
    cursorObject.execute("INSERT INTO adminlogin WHERE Name = %s AND Password = %s", [username, password])