from django.urls import path, include
from . import views

app_name = 'company'

urlpatterns = [
    path('', views.company_login, name='index'),
    path('home/', views.company_login, name='home'),
    path('forum/', views.forum, name='Forum'), 
    path('send_message/', views.send_message, name='send_message'),
    path('jobs/', views.jobs, name='posted'),
    path('post_job/', views.post_job, name='post_job'),
    path('applicants/', views.applicants, name='applicants')
]
'''
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
]
'''