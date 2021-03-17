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
]
