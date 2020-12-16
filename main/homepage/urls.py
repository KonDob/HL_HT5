from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('students_list/', views.student_list, name='students_list')
]
