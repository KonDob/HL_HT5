from django.urls import path

from . import views
from .views import SignUpView, ActivateView, SignOutView, SignInView

app_name = 'homepage'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('students_list/', views.StudentListView.as_view(),
         name='students_list'),
    path('create_student/', views.CreateStudentView.as_view(),
         name='create_student'),
    path('edit_student/<id>', views.EditStudentView.as_view(),
         name='edit_student'),

    path('books', views.BooksView.as_view(), name='books'),
    path('edit_book/<id>', views.EditBook.as_view(), name='edit_book'),
    path('delete_book/<id>', views.EditBook.as_view(), name='delete_book'),
    path('update_book/<id>', views.EditBook.as_view(), name='update_book'),

    path('subjects', views.SubjectsView.as_view(), name='subjects'),
    path('subject/<id>', views.SubjectInfoView.as_view(), name='add_student'),
    path('subject/<id>', views.SubjectInfoView.as_view(),
         name='delete_subject'),
    path('subject/<id>', views.SubjectInfoView.as_view(),
         name='edit_subject_name'),
    path('subject/<id>', views.SubjectInfoView.as_view(), name='subject_info'),

    path('teachers', views.TeachersView.as_view(), name='teachers'),
    path('teacher/<id>', views.TeacherDetailView.as_view(),
         name='teacher_detail'),
    path('teacher/<id>', views.TeacherDetailView.as_view(),
         name='delete_teacher'),
    path('teacher/<id>', views.TeacherDetailView.as_view(),
         name='add_student'),
    path('teacher/<id>', views.TeacherDetailView.as_view(),
         name='edit_teachers_name'),
    path('json_students_list', views.JsonStudentView.as_view(),
         name='json_students_list'),
    path('csv_students_list', views.CSVStudentView.as_view(),
         name='csv_students_list'),
    path('sign_up', SignUpView.as_view(), name='sign_up_view'),
    path('sign_out', SignOutView.as_view(), name='sign_out_view'),
    path('login', SignInView.as_view(), name='login'),
    path('activate/<uid>/<token>', ActivateView.as_view(),
         name='sign_up_view'),
]
