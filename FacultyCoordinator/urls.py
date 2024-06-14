from django.urls import path, include
from . import views

app_name = 'facultyCo'

urlpatterns = [
    path('', views.facultyCo_login, name='index'),
    path('home/', views.facultyCo_login, name='home'),
    path('import-student-data/', views.import_student_data, name='import_student_data'),
    path('add_lecture_material/', views.add_lecture_material, name='add_lecture_material'),
    path('learning/', views.learning, name='learning'),
    path('forum/', views.forum, name='forum')
]