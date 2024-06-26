from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db import connection
from .models import Job
import mysql.connector
from django.conf import settings

def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('enrollment_no')
        password = request.POST.get('mobile_no')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM student_data WHERE Enrollment_No = %s AND Mobile_No = %s", [username, password])
            user = cursor.fetchone()
            
        with connection.cursor() as cursor:
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
                
        if user:
            # Authentication successful
            request.session['user'] = user
            student_name = user[1]
            return render(request, 'student_index.html', {'student_name': student_name, 'usernames': usernames, 'messages': messages})  # Render student coordinnator panel page
        else:
            # Authentication failed
            messages.error(request, 'Invalid username or password')

    return render(request, 'student_login.html')

def forum(request):
    user = request.session.get('user')
    usernames = request.session.get('usernames')
    student_name = user[1]

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

    return render(request, 'student_index.html', {'student_name': student_name, 'usernames': usernames, 'messages': messages})

def jobs(request):
    user = request.session.get('user')
    student_name = user[1]
    '''
    use PlacementCellDB;
    CREATE TABLE Jobs (Company_ID VARCHAR(10), Company_Name VARCHAR(255), Domain VARCHAR(25), Job_Description VARCHAR(255), Min_Salary VARCHAR(10), Max_Salary VARCHAR(10), Job_Type VARCHAR(20), Location VARCHAR(25), Eligibility_Criteria SMALLINT(5), Email_Address VARCHAR(25), Phone VARCHAR(10), Application_Link VARCHAR(255));

    INSERT INTO Jobs (Company_ID, Company_Name, Domain, Job_Description, Min_Salary, Max_Salary, Job_Type, Location, Eligibility_Criteria, Email_Address, Phone) 
    VALUES ('ABC123', 'ABC Corporation', 'Software Development', 'This is the description of the job!', '50000', '60000', 'Full-time', 'Ahmedabad', 6.00, 'abc@example.com', '1234567890');
    
    select * from Jobs;
    '''
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
    return render(request, 'jobs.html', {'student_name': student_name, 'job_data': job_data})

def learning(request):
    user = request.session.get('user')
    student_name = user[1]

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Learning_material")
        material = cursor.fetchall()
        material_data = []
        for row in material:
            material_heading, material_description, material_link, file = row[:4]
            
            material_dict = {
                'material_heading': material_heading,
                'material_description': material_description,
                'material_link': material_link,
                'file': file
            }
            print(file)

            material_data.append(material_dict)

    return render(request, 'learning.html', {'student_name': student_name, 'material_data': material_data})

def profile(request):
    user = request.session.get('user')
    er_no, name, gender, mob_no, email_add, branch, sem = user[:7]
    print(user)
    return render(request, 'student_profile.html', {
        'er_no': er_no,
        'name': name,
        'gender': gender,
        'mob_no': mob_no,
        'email_add': email_add,
        'branch': branch,
        'sem': sem,
    })

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


def send_message(request):
    user = request.session.get('user')
    user_name = user[1]
    message = request.POST.get('message')
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO Messages (Username, Message) VALUES (%s, %s)", (user_name, message))
    
    user = request.session.get('user')
    usernames = request.session.get('usernames')
    student_name = user[1]

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

    return render(request, 'student_index.html', {'student_name': student_name, 'usernames': usernames, 'messages': messages})

def apply(request):
    dataBase = mysql.connector.connect(     # Connect to MySQL Database
        host='localhost',
        user='root',
        passwd='TIGER',
        database='placementcelldb'
    )
    user = request.session.get('user')
    er_no = user[0]
    company_id = request.POST.get('company_id')

    cursorObject = dataBase.cursor()
    
    # Insert Data into Table query
    cursorObject.execute("INSERT INTO Applied_Jobs (Er_no, Company_ID) VALUES (%s, %s)", (er_no, company_id))

    # Commit Changes to the Database
    dataBase.commit()

    # Close Cursor and Database Connection
    cursorObject.close()
    dataBase.close()
    return render(request, 'student_index.html')

from django.http import FileResponse, HttpResponse
import os

def serve_file(request, file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = FileResponse(f, as_attachment=True)
            return response
    else:
        # Handle file not found error
        return HttpResponse("File not found")