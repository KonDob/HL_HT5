from django.shortcuts import render, redirect

from .forms import StudentForm
from .models import Student


def home(request):
    """
    Return html page
    """
    return render(request, 'home.html')


def student_list(request):
    students = Student.objects.all()
    return render(request, 'students_list.html', {'students': students})


def create_student_by_form(request):
    """
    Create student by Django Forms
    """

    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student_form.save()
            return redirect('homepage:students_list')

    elif request.method == 'GET':
        form = StudentForm()
        context = {'form': form}
        return render(request, 'student_form.html', context=context)
