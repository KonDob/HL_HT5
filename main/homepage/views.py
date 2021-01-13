from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.base import View

from .forms import StudentForm
from .models import Student, Book


class HomePageView(View):

    template_name = 'home.html'

    def get(self, request):
        """
        Return html page
        """
        return render(request, self.template_name)


class StudentListView(View):

    template_name = 'students_list.html'

    def get(self, request):
        students = Student.objects.all()
        return render(request, self.template_name, {'students': students})


class CreateStudentView(View):
    """
    Create student by Django Forms
    """

    template_name = 'student_form.html'

    def get(self, request):
        form = StudentForm()
        context = {'form': form}
        return render(request, self.template_name, context=context)

    def post(self, request):
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student_form.save()
            return redirect('homepage:students_list')
        else:
            messages.add_message(request, 'Your form of student creation isn`t \
                                 valid')
            return self.get(request, id)


class EditStudentView(View):

    def get(self, request, id):
        student = Student.objects.get(id=id)
        student_form = StudentForm(instance=student)
        context = {
            'form': student_form,
            'id': id,
        }
        return render(request, 'edit_student.html', context=context)

    def post(self, request, id):
        student = Student.objects.get(id=id)
        student_form = StudentForm(request.POST, instance=student)
        if student_form.is_valid():
            student_form.save()
            return redirect('homepage:students_list')
        else:
            messages.add_message(request, messages.INFO,
                                 'You trying edit student with invalid data')
            return self.get(request, id)


class BooksView(View):
    """
        Page to see all books and additional info about books owner
    """

    def get(self, request):

        books = Book.objects.all()

        context = {
            'books': books
        }
        return render(request, 'books_view.html', context=context)