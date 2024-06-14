from django.shortcuts import render                     # To Render html files
from django.contrib import messages                     # Showing Error Messages
from django.db import connection                        # Default Database Handler of Django
import pandas as pd                                     # To manage large data from xlsx file
import mysql.connector                                  # Database Hnadler for MySQL
from django.core.files.storage import FileSystemStorage # Save xlsx file on server side (Laptop)


def facultyCo_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            # Query the MySQL table
            cursor.execute("SELECT * FROM facultyCo_data WHERE EmpId = %s AND Password = %s", [username, password])
            user = cursor.fetchone()

        if user:
            request.session['user'] = user
            facultyco_name = user[1]
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Learning_Material")
                materials = cursor.fetchall()
                material_data = []
                for row in materials:
                    heading, description, link = row[:3]

                    material_dict = {
                        'heading': heading,
                        'description': description,
                        'link': link,
                    }

                    material_data.append(material_dict)
                return render(request, 'facultyCo_index.html', {'facultyco_name': facultyco_name,'material_data': material_data})
        else:
            # Authentication failed
            messages.error(request, 'Invalid username or password')


    return render(request, 'facultyCo_login.html')


# On pressing the "Import Data" button, after uploading the file
def import_student_data(request):
    uploaded_file = request.FILES['file']
    fs = FileSystemStorage()

    filename = 'StudentData.xlsx'           # File from user saved as FacultyCoData.xlsx
    fs.save(filename, uploaded_file)
    file_path = fs.path(filename)
    
    df = pd.read_excel('StudentData.xlsx')  # Read Excel file into a Pandas DataFrame

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
    cursorObject.execute(table_creation_query)
    
    # Insert Data into Table query
    query = 'INSERT INTO Student_Data (Enrollment_No, Name, Gender, Mobile_No, Email_Address, Branch, Semester) VALUES (%s, %s, %s, %s, %s, %s, %s)'

    # Iterate through DataFrame and execute INSERT query for each row
    for row in df.itertuples():
        cursorObject.execute(query, (row.Enrollment_No, row.Name, row.Gender, row.Mobile_No, row.Email_Address, row.Branch, row.Semester))

    # Commit Changes to the Database
    dataBase.commit()

    # Close Cursor and Database Connection
    cursorObject.close()
    dataBase.close()

    return render(request, 'facultyCo_index.html')      # Redirect back to facultyCo_index.html


def add_lecture_material(request):
    heading = request.POST.get('heading')
    description = request.POST.get('description')
    link = request.POST.get('link')

    print("Details", heading, description, link)
    # CREATE TABLE Learning_Material (Heading VARCHAR(255), Material_Description VARCHAR(255), Link VARCHAR(255));
    with connection.cursor() as cursor:
        # Insert INTO learning_material (Heading, Material_Description, Link)
        # VALUES ('TCS Interview Questions', 'Here are the most frequently asked interview questions by Tata Consultancy Services.', 'https://blog.internshala.com/tcs-interview-questions/');

        cursor.execute("Insert INTO learning_material (Heading, Material_Description, Link) VALUES (%s, %s, %s)", [heading, description, link])
    return render(request, 'facultyCo_index.html')

def forum(request):
    user = request.session.get('user')
    usernames = request.session.get('usernames')
    facultyco_name = user[1]

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

    return render(request, 'forum_fco.html', {'facultyco_name': facultyco_name, 'usernames': usernames, 'messages': messages})


def learning(request):
    user = request.session.get('user')
    request.session['user'] = user
    facultyco_name = user[1]
    with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Learning_Material")
                materials = cursor.fetchall()
                material_data = []
                for row in materials:
                    heading, description, link = row[:3]

                    material_dict = {
                        'heading': heading,
                        'description': description,
                        'link': link,
                    }

                    material_data.append(material_dict)
                return render(request, 'facultyCo_index.html', {'facultyco_name': facultyco_name,'material_data': material_data})