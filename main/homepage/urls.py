from django.urls import path

from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('students_list/', views.StudentListView.as_view(),
         name='students_list'),
    path('create_student/', views.CreateStudentView.as_view(),
         name='create_student'),
    path('edit_student/<id>', views.EditStudentView.as_view(),
         name='edit_student'),
    path('json_students_list', views.JsonStudentView.as_view(),
         name='json_students_list'),
    path('csv_students_list', views.CSVStudentView.as_view(),
         name='csv_students_list'),
    path('send_email', views.SendMailView.as_view(),
         name='send_email'),
]
