from django.urls import path
from . import views

app_name = 'TPPOfficer'

urlpatterns = [
    path('', views.admin_login, name='index'),
    path('home/', views.admin_login, name='home'), 
    path('import-facultyCo-data/', views.import_facultyCo_data, name='import_facultyCo_data'),
    path('import-studentCo-data/', views.import_studentCo_data, name='import_studentCo_data'),
    path('import_admin/', views.import_admin, name='import_admin'),
    path('addadmin/', views.addadmin, name='addadmin'),
    path('add_admin/', views.add_admin, name='add_admin'),
    path('manageadmin/', views.manageadmin, name='manageadmin'),
    path('managejobs/', views.managejobs, name='managejobs'),
    path('managejobs/<str:company_id>/', views.job_details, name='job_details'),
    path('managefaculty/', views.managefaculty, name='managefaculty'),
    path('addfaculty/', views.addfaculty, name='addfaculty'),
    path('import_faculty/', views.import_faculty, name='import_faculty'),
    path('add_faculty/', views.add_faculty, name='add_faculty'),
]