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
    path('books', views.BooksView.as_view(), name='books_view'),
]
