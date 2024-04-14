from django.shortcuts import render
from django.contrib import messages
from django.db import connection

def studentCo_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            # Query the MySQL table
            cursor.execute("SELECT * FROM StudentCo_Data WHERE Enrollment_No = %s AND Password = %s", [username, password])
            user = cursor.fetchone()

        if user:
            # Authentication successful
            return render(request, 'studentCo_index.html')  # Render student coordinnator panel page
        else:
            # Authentication failed
            messages.error(request, 'Invalid username or password')

    return render(request, 'studentCo_login.html')