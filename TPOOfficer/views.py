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

        with connection.cursor() as cursor:
            # Query the MySQL table
            cursor.execute("SELECT * FROM student_data")
            usernames = [row[1] for row in cursor.fetchall()]
            request.session['usernames'] = usernames
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Messages")
            fetched_messages = cursor.fetchall()
            messages = []
            for row in fetched_messages:
                Username, Message = row[:2]

                message_dict = {
                    'Username': Username,
                    'Message': Message
                }
                messages.append(message_dict)
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Admin_data")
            admin_rows = cursor.fetchall()  # Fetch all rows from the Admin_data table

        admin_data = []  # Initialize an empty list to store admin data dictionaries

        # Iterate over fetched rows
        for row in admin_rows:
            Name, Password = row[:2]
            # Create a dictionary for each admin record
            admin_dict = {
                'Name': Name,
                'Password': Password,
            }
            admin_data.append(admin_dict)  # Append the dictionary to the admin_data list



        if user:                                        # Authentication Success, user exixts
            request.session['user'] = user
            admin_name = user[0]
            return render(request, 'admin_index.html', {'admin_name': admin_name, 'usernames': usernames, 'messages': messages, 'admin_data':admin_data})  # Render student coordinnator panel page
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

    filename = 'Student_Data.xlsx'           # File from user saved as StudentData.xlsx
    fs.save(filename, uploaded_file)
    file_path = fs.path(filename)
    
    df = pd.read_excel('Student_Data.xlsx')  # Read Excel file into a Pandas DataFrame

    dataBase = mysql.connector.connect(     # Connect to MySQL Database
        host='localhost',
        user='root',
        passwd='TIGER',
        database='placementcelldb'
    )

    cursorObject = dataBase.cursor()        # Object of Cursor

    # deletes table / previous data if exist
    drop_table = 'DROP TABLE IF EXISTS Student_Data'
    cursorObject.execute(drop_table)

    # Create Table (If already haven't)
    table_creation_query = 'CREATE TABLE IF NOT EXISTS Student_Data (Enrollment_No varchar(11), Name varchar(255), Gender varchar(6), Mobile_No varchar(10), Email_Address varchar(25), Branch varchar(25), Semester varchar(2))'
    # table_creation_query = 'CREATE TABLE IF NOT EXISTS StudentCo_Data (Enrollment_No varchar(11), Password varchar(7))'
    cursorObject.execute(table_creation_query)
    
    # Insert Data into Table query
    query = 'INSERT INTO Student_Data (Enrollment_No, Name, Gender, Mobile_No, Email_Address, Branch, Semester) VALUES (%s, %s, %s,%s, %s, %s, %s)'

    # Iterate through DataFrame and execute INSERT query for each row
    for row in df.itertuples():
        cursorObject.execute(query, (row.Enrollment_No, row.Name, row.Gender, row.Mobile_No, row.Email_Address, row.Branch, row.Semester))

    # Commit Changes to the Database
    dataBase.commit()

    # Close Cursor and Database Connection
    cursorObject.close()
    dataBase.close()

    return render(request, 'admin_index.html')      # Redirect back to admin_index.html


def addadmin(request):
    user = request.session.get('user')
    admin_name = user[0]
    return render (request, 'addadmin.html', {'admin_name': admin_name})


# wrong method
def import_admin(request):
    uploaded_file = request.FILES['file']
    fs = FileSystemStorage()

    filename = 'Admin_Data.xlsx'           # File from user saved as StudentData.xlsx
    fs.save(filename, uploaded_file)
    file_path = fs.path(filename)
    
    df = pd.read_excel('Admin_Data.xlsx')  # Read Excel file into a Pandas DataFrame

    dataBase = mysql.connector.connect(     # Connect to MySQL Database
        host='localhost',
        user='root',
        passwd='TIGER',
        database='placementcelldb'
    )

    cursorObject = dataBase.cursor()        # Object of Cursor

    # deletes table / previous data if exist
    drop_table = 'DROP TABLE IF EXISTS Admin_Data'
    cursorObject.execute(drop_table)

    # Create Table (If already haven't)
    table_creation_query = 'CREATE TABLE IF NOT EXISTS Admin_Data (Name varchar(15), Password varchar(7))'
    # table_creation_query = 'CREATE TABLE IF NOT EXISTS StudentCo_Data (Enrollment_No varchar(11), Password varchar(7))'
    cursorObject.execute(table_creation_query)
    
    # Insert Data into Table query
    query = 'INSERT INTO Admin_Data (Name, Password) VALUES (%s, %s)'

    # Iterate through DataFrame and execute INSERT query for each row
    for row in df.itertuples():
        cursorObject.execute(query, (row.Name, row.Password))

    # Commit Changes to the Database
    dataBase.commit()

    # Close Cursor and Database Connection
    cursorObject.close()
    dataBase.close()


    return render(request, 'admin_index.html')

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
    insert_query = "INSERT INTO admin_data (Name, Password) VALUES (%s, %s)"
    cursorObject.execute(insert_query, (username, password))
    
    dataBase.commit()  # Committing the transaction

    cursorObject.close()  # Closing cursor
    dataBase.close()  # Closing database connection

    return render(request, 'admin_index.html')

def manageadmin(request):
    user = request.session.get('user')
    admin_name = user[0]

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Admin_data")
        admin_rows = cursor.fetchall()  # Fetch all rows from the Admin_data table

    admin_data = []  # Initialize an empty list to store admin data dictionaries

        # Iterate over fetched rows
    for row in admin_rows:
        Name, Password = row[:2]
        # Create a dictionary for each admin record
        admin_dict = {
            'Name': Name,
            'Password': Password,
        }
        admin_data.append(admin_dict)  # Append the dictionary to the admin_data list

    return render(request, 'admin_index.html', {'admin_name': admin_name, 'admin_data': admin_data})

def managejobs(request):
    user = request.session.get('user')
    admin_name = user[0]
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Jobs")
        jobs = cursor.fetchall()
        job_data = []
        for row in jobs:
            Company_ID, Company_Name, Domain, Job_Description, Min_Salary, Max_Salary, Job_Type, Location, Eligibility_Criteria, Email_Address, Phone, Application_Link = row[:12]

            job_dict = {
                'Company_ID': Company_ID,
                'Company_Name': Company_Name,
                'Domain': Domain,
                'Job_Description': Job_Description,
                'Min_Salary': Min_Salary,
                'Max_Salary': Max_Salary,
                'Job_Type': Job_Type,
                'Location': Location,
                'Eligibility_Criteria': Eligibility_Criteria,
                'Email_Address': Email_Address,
                'Phone': Phone,
                'Application_Link': Application_Link
            }

            job_data.append(job_dict)
    return render(request, 'managejobposts.html', {'admin_name': admin_name, 'job_data': job_data})


def job_details(request, company_id):
    with connection.cursor() as cursor:
        # Execute SQL query with parameterized values
        cursor.execute("SELECT * FROM Jobs WHERE Company_ID=%s", [company_id])
            
            # Fetch one row from the query result
        job = cursor.fetchone()
        Company_ID, Company_Name, Domain, Job_Description, Min_Salary, Max_Salary, Job_Type, Location, Eligibility_Criteria, Email_Address, Phone, Application_Link = job[:12]

        job_data = {
            'Company_ID': Company_ID,
            'Company_Name': Company_Name,
            'Domain': Domain,
            'Job_Description': Job_Description,
            'Min_Salary': Min_Salary,
            'Max_Salary': Max_Salary,
            'Job_Type': Job_Type,
            'Location': Location,
            'Eligibility_Criteria': Eligibility_Criteria,
            'Email_Address': Email_Address,
            'Phone': Phone,
            'Application_Link': Application_Link
        }

        # Check if any row was fetched
    if job:
        return render(request, 'job_profile.html', {'job': job_data})
    else:
        return render(request, 'no_job_found.html')  # Render a template indicating no job found


def managefaculty(request):
    user = request.session.get('user')
    admin_name = user[0]
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM FacultyCo_data")
        facultyco_rows = cursor.fetchall()  # Fetch all rows from the Admin_data table

    facultyco_data = []  # Initialize an empty list to store admin data dictionaries

        # Iterate over fetched rows
    for row in facultyco_rows:
        EmpID, Name = row[:2]
        # Create a dictionary for each admin record
        facultyco_dict = {
            'EmpID': EmpID,
            'Name': Name,
        }
        facultyco_data.append(facultyco_dict)  # Append the dictionary to the admin_data list

    return render(request, 'managefaculty.html', {'admin_name': admin_name, 'facultyco_data': facultyco_data})

def addfaculty(request):
    user = request.session.get('user')
    admin_name = user[0]
    return render(request, 'addfaculty.html', {'admin_name': admin_name})

def import_faculty(request):
    user = request.session.get('user')
    admin_name = user[0]

    uploaded_file = request.FILES['file']
    fs = FileSystemStorage()

    filename = 'FacultyCo_Data.xlsx'           # File from user saved as StudentData.xlsx
    fs.save(filename, uploaded_file)
    file_path = fs.path(filename)
    
    df = pd.read_excel('FacultyCo_Data.xlsx')  # Read Excel file into a Pandas DataFrame

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
    table_creation_query = 'CREATE TABLE IF NOT EXISTS FacultyCo_Data (EmpID varchar(10), Name Varchar(15), Password varchar(10))'
    # table_creation_query = 'CREATE TABLE IF NOT EXISTS StudentCo_Data (Enrollment_No varchar(11), Password varchar(7))'
    cursorObject.execute(table_creation_query)
    
    # Insert Data into Table query
    query = 'INSERT INTO FacultyCo_Data (EmpID, Name, Password) VALUES (%s, %s, %s)'

    # Iterate through DataFrame and execute INSERT query for each row
    for row in df.itertuples():
        cursorObject.execute(query, (row.EmpID, row.Name, row.Password))

    # Commit Changes to the Database
    dataBase.commit()

    # Close Cursor and Database Connection
    cursorObject.close()
    dataBase.close()

    return render(request, 'managefaculty.html', {'admin_name': admin_name})

def add_faculty(request):
    empid = request.POST.get('emp_id')
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
    insert_query = "INSERT INTO facultyco_data (EmpID, Name, Password) VALUES (%s, %s, %s)"
    cursorObject.execute(insert_query, (empid, username, password))
    
    dataBase.commit()  # Committing the transaction

    cursorObject.close()  # Closing cursor
    dataBase.close()  # Closing database connection

    return render(request, 'managefaculty.html')