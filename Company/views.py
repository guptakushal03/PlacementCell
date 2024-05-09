from django.shortcuts import render
from django.contrib import messages
from django.db import connection

def company_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            # Query the MySQL table
            cursor.execute("SELECT * FROM job_data WHERE Company_Name = %s AND Pass = %s", [username, password])
            user = cursor.fetchone()
        
        if user:
            # Authentication successful
            request.session['user'] = user
            company_name = user[1]
            
            return render(request, 'company_index.html', {'company_name': company_name})  # Render admin panel page
        else:
            # Authentication failed
            messages.error(request, 'Invalid username or password')

    return render(request, 'company_login.html')

