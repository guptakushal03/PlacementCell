from django.urls import path, include
from . import views

app_name = 'student'

urlpatterns = [
    path('', views.student_login, name='index'),
    path('home/', views.student_login, name='home'), 
    path('forum/', views.forum, name='Forum'), 
    path('jobs/', views.jobs, name='posted'), 
    path('learning/', views.learning, name='learning'), 
    path('student_profile/', views.profile, name='profile'), 
    path('jobs/<str:company_id>/', views.job_details, name='job_details'),
    # path('save-message/', views.save_message, name='save_message'),
    path('send_message/', views.send_message, name='send_message'),
    path('apply/', views.apply, name='apply'),
    #path('serve_file/<path:file_path>', views.serve_file, name='serve_file'),
]