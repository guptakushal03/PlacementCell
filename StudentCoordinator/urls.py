from django.urls import path
from . import views

app_name = 'studentCo'

urlpatterns = [
    path('', views.studentCo_login, name='index'),
    path('home/', views.studentCo_login, name='home'), 
]