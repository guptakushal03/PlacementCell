from django.urls import path, include
from . import views

app_name = 'company'

urlpatterns = [
    path('', views.company_login, name='index'),
    path('home/', views.company_login, name='home'),
]