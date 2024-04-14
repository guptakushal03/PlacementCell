from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('TPOOfficer/', include('TPOOfficer.urls')),
    path('FacultyCoordinator/', include('FacultyCoordinator.urls')),
    path('StudentCoordinator/', include('StudentCoordinator.urls')),
    path('Company/', include('Company.urls')),
    path('Student/', include('Student.urls')),
]
