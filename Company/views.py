from django.shortcuts import render
from django.contrib import messages
from django.db import connection

def company_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usernames = request.session.get('usernames')

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
            cursor.execute("SELECT * FROM job_data WHERE Company_ID = %s AND Pass = %s", [username, password])
            user = cursor.fetchone()
        
        if user:
            request.session['user'] = user
            company_name = user[0]
            
            return render(request, 'company_index.html', {'company_name': company_name, 'usernames': usernames, 'messages': messages})  # Render admin panel page
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'company_login.html')


def forum(request):
    user = request.session.get('user')
    usernames = request.session.get('usernames')
    company_name = user[0]

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

    return render(request, 'company_index.html', {'company_name': company_name, 'usernames': usernames, 'messages': messages})

def send_message(request):
    user = request.session.get('user')
    user_name = user[1]
    message = request.POST.get('message')
    
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO Messages (Username, Message) VALUES (%s, %s)", (user_name, message))
    
    user = request.session.get('user')
    usernames = request.session.get('usernames')
    company_name = user[0]

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

    return render(request, 'company_index.html', {'company_name': company_name, 'usernames': usernames, 'messages': messages})

def post_job(request):
    user = request.session.get('user')
    company_id = user[0]
    company_name = user[1]
    jobDomain = request.POST.get('jobDomain')
    jobDescription = request.POST.get('jobDescription')
    minSalary = request.POST.get('minSalary')
    maxSalary = request.POST.get('maxSalary')
    jobType = request.POST.get('jobType')
    location = request.POST.get('location')
    eligibility_criteria = request.POST.get('eligibility')
    email = request.POST.get('email')
    phone = request.POST.get('number')

    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO Jobs (Company_ID, Company_Name, Domain, Job_Description, Min_Salary, Max_Salary, Job_Type, Location, Eligibility_Criteria, Email_Address, Phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (company_id, company_name, jobDomain, jobDescription, minSalary, maxSalary, jobType, location, eligibility_criteria, email, phone))
    
    return render(request, 'company_index.html', {'company_name': company_name})

def jobs(request):
    user = request.session.get('user')

    '''
    use PlacementCellDB;
    CREATE TABLE Jobs (Company_ID VARCHAR(10), Company_Name VARCHAR(255), Domain VARCHAR(25), Job_Description VARCHAR(255), Min_Salary VARCHAR(10), Max_Salary VARCHAR(10), Job_Type VARCHAR(20), Location VARCHAR(25), Eligibility_Criteria SMALLINT(5), Email_Address VARCHAR(25), Phone VARCHAR(10), Application_Link VARCHAR(255));

    INSERT INTO Jobs (Company_ID, Company_Name, Domain, Job_Description, Min_Salary, Max_Salary, Job_Type, Location, Eligibility_Criteria, Email_Address, Phone) 
    VALUES ('ABC123', 'ABC Corporation', 'Software Development', 'This is the description of the job!', '50000', '60000', 'Full-time', 'Ahmedabad', 6.00, 'abc@example.com', '1234567890');
    
    select * from Jobs;
    
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
            '''
    return render(request, 'job_posting.html')

def applicants(request):
    user = request.session.get('user')
    company_id = user[0]
    company_name = user[0]
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM applied_jobs where Company_id = %s",[company_id])
        data = cursor.fetchall()
        erno = [row[0] for row in data]

        # Fetch student data for each enrollment number
        stu_data = []
        for enrollment_number in erno:
            cursor.execute("SELECT * from student_data where enrollment_no = %s", [enrollment_number])
            stu_data.extend(cursor.fetchall())

        student_data=[]
        for stu in stu_data:
            Enrollment_No, Name, Gender, Mobile_No, Email_Address, Branch, Semester = stu[:7]

            stu_dict = {
                'Enrollment_No': Enrollment_No,
                'Name': Name,
                'Gender': Gender,
                'Mobile_No': Mobile_No,
                'Email_Address': Email_Address,
                'Branch': Branch,
                'Semester': Semester
            }
            student_data.append(stu_dict)


    return render(request, 'applicants.html', {'company_name': company_name, 'stu_data':student_data})