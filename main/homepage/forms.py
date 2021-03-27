from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Student, Book, Subject, Teacher


class StudentForm(ModelForm):

    class Meta:
        model = Student
        fields = ['name', 'surname', 'normalized_name', 'social_url', 'age',
                  'sex', 'address', 'birthday', 'email', 'description']


class UserSignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class BookForm(ModelForm):

    class Meta:
        model = Book
        fields = ['name']


class SubjectForm(ModelForm):

    class Meta:
        model = Subject
        fields = ['title']


class TeacherForm(ModelForm):

    class Meta:
        model = Teacher
        fields = ['name']
