from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import DetailView
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import *

from .forms import StudentForm, BookForm, SubjectForm, TeacherForm
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

    def post(self, request):  # noqa
        template_name = 'students_list.html'
        if request.POST.get('filter_by', '') == 'filter_by_teacher':

            students = Student.objects.filter(
                teacher__name=request.POST.get('text_form', '')
            )

            return render(request, template_name=self.template_name, context={
                'students': students})

        elif request.POST.get('filter_by', '') == 'filter_by_subject':

            students = Student.objects.filter(
                subject__name_of_subject=request.POST.get('text_form', '')
            )

            return render(request, template_name=self.template_name, context={
                'students': students})

        elif request.POST.get('filter_by', '') == 'filter_by_book':

            students = Student.objects.filter(
                book__id=request.POST.get('text_form', '')
            )

            return render(request, template_name=self.template_name, context={
                'students': students})

        return redirect('homepage:students_list')


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

    def get(self, request, id):  # noqa
        book = Book.objects.get(id=id)
        book_form = BookForm(instance=book)
        context = {
            'form': book_form,
            'id': id,
        }
        return render(request, 'edit_book.html', context=context)

    def post(self, request, id):  # noqa
        book = Book.objects.get(id=id)
        book.delete()
        context = {'book': book,
                   'book_id': book.id}
        return redirect('homepage:books')

    def put(self, request, id):  # noqa
        book = Book.objects.get(id=id)
        book_form = BookForm(instance=book)
        if book_form.is_valid():
            book_form = BookForm(instance=book)
            book_form.save(commit=False)
            book_form.id = id
            book_form.save()
            return redirect('homepage:books')
        else:
            messages.add_message(request, messages.INFO,
                                 'You trying edit books with invalid data')
            return self.get(request, id)


class SubjectsView(ListView):
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


class SubjectInfoView(DetailView):
    """
        Page to see choose subject and additional info about it.
    """
    model = Subject
    template_name = 'subject_info.html'

    def get(self, request, id):  # noqa
        subject = Subject.objects.get(id=id)
        subject_form = SubjectForm(instance=subject)
        subject_student = Student.objects.filter(subject=subject.id)
        new_student = Student.objects.exclude(subject=subject.id)
        context = {'subject_id': subject.id,
                   'subject_title': subject.title,
                   'form_subject': subject_form,
                   'subject_student': subject_student,
                   'new_student': new_student}
        return render(request, 'subject_info.html', context=context)

    def post(self, request, id):
        if 'add' in request.POST:
            subject = Subject.objects.get(id=id)
            student = Student.objects.get(id=request.POST.get('add', ''))
            student.subject = subject
            student.save()

        if 'edit' in request.POST:
            subject = SubjectForm(request.POST)
            pre_save_subject = subject.save(commit=False)
            pre_save_subject.id = id
            pre_save_subject.save()

        elif 'delete' in request.POST:
            student = Student.objects.get(id=request.POST.get('delete', ''))
            subject = student.subject
            subject.student_set.remove(student)

        return redirect('homepage:subjects')


class TeachersView(ListView):
    """[summary]

    Args:
        View ([type]): [description]
    """
    model = Teacher

    template_name = 'teachers.html'


class TeacherDetailView(View):

    template_name = 'teacher_detail.html'

    def get(self, request, id):
        teacher = Teacher.objects.get(id=id)
        teacher_form = TeacherForm(instance=teacher)
        teachers_students = Student.objects.filter(teacher=teacher.id)
        new_students = Student.objects.exclude(teacher=teacher.id)
        context = {'teacher_form': teacher_form,
                   'teacher_id': teacher.id,
                   'teacher': teacher,
                   'teachers_students': teachers_students,
                   'new_students': new_students}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, id):  # noqa
        if 'edit' in request.POST:
            teacher = TeacherForm(request.POST)
            pre_save_teacher = teacher.save(commit=False)
            pre_save_teacher.id = id
            pre_save_teacher.save()

        elif 'add' in request.POST:
            teacher = Teacher.objects.get(id=id)
            student = Student.objects.get(id=request.POST.get('add', ''))
            teacher.students.add(student)
            teacher.save()

        elif 'delete' in request.POST:
            student = Student.objects.get(id=request.POST.get('delete', ''))
            teacher = Teacher.objects.get(student=student)
            teacher.student.remove(student)

        return redirect('homepage:teachers')
