from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import *

from .forms import StudentForm, BookForm
from .models import Student, Book, Subject, Teacher


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
            'books': books,
            }
        return render(request, 'books_view.html', context=context)


class EditBook(View):

    def get(self, request, id):
        book = Book.objects.get(id=id)
        book_form = BookForm(instance=book)
        context = {
            'form': book_form,
            'id': id,
        }
        return render(request, 'edit_book.html', context=context)

    def put(self,request, id):
        book = Book.objects.get(id=id)
        book_form = BookForm(instance=book)
        if book_form.is_valid():
            book_form.save()
            return redirect('homepage:books')
        else:
            messages.add_message(request, messages.INFO,
                                 'You trying edit books with invalid data')
            return self.get(request, id)

    def delete(self, request, id):
        id = int(id)
        book = Book.objects.get(id=id)
        book_form = BookForm(instance=book)
        try:
            book_form.delete()
            return redirect('homepage:books')
        except:
          messages.add_message(request, messages.INFO,
                                 'You trying edit books with invalid data')

class DeleteBook(DeleteView):

    model = Book
    fields = ['name']
    template_name = 'edit_book.html'


class SubjectView(ListView):

    """
        Page to see all subjects and additional info about subjects owner
    """
    model = Subject

    template_name = 'subjects.html'

    # def get(self, request):

    #     subjects = self.model.objects.all()

    #     context = {
    #         'subjects': subjects
    #     }
    #     return render(request, 'subjects.html', context=context)


class TeachersView(ListView):
    """[summary]

    Args:
        View ([type]): [description]
    """
    model = Teacher

    template_name = 'teachers.html'

    # def get(self, request):

    #     teachers = self.model.objects.all()
    
    #     context = {
    #         'teachers': teachers
    #     }
    #     return render(request, 'teachers.html', context=context)

