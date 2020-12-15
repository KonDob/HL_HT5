from django.shortcuts import render
from .models import Student

# Create your views here.

def home(request):
    """
    Return html page
    """
    return render(request, 'home.html')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'students_list.html', {'students': students})