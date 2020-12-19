from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('students_list/', views.student_list, name='students_list'),
    path('create_student/', views.create_student_by_form,
         name='create_student'),
    path('edit_student/<id>', views.edit_student, name='edit_student')
]
