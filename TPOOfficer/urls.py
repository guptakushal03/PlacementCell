from django.urls import path
from . import views

app_name = 'TPPOfficer'

urlpatterns = [
    path('', views.admin_login, name='index'),
    path('home/', views.admin_login, name='home'), 
    path('import-facultyCo-data/', views.import_facultyCo_data, name='import_facultyCo_data'),
    path('import-studentCo-data/', views.import_studentCo_data, name='import_studentCo_data'),
    path('addadmin/', views.addadmin, name='addadmin'),
]