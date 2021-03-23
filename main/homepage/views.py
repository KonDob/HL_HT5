import csv
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, ListView, \
    UpdateView, DetailView
from django.conf import settings

from .models import Student
from .emails import send_email
from django.core.cache import cache
from django.shortcuts import redirect, render

from django.views.generic import DetailView
from django.views.generic.base import View
from django.views.generic.edit import * # noqa
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings

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
    model = Student
    template_name = 'students_list.html'


class CreateStudentView(CreateView):
    def post(self, request):  # noqa
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
    model = Student
    template_name = 'student_form.html'
    fields = ['name', 'social_url', 'surname']
    success_url = reverse_lazy('homepage:students_list')


class EditStudentView(UpdateView):

    model = Student
    template_name = 'edit_student.html'
    fields = ['name', 'social_url', 'surname']
    success_url = reverse_lazy('homepage:students_list')


class DetailsStudentView(DetailView):

    model = Student
    template_name = 'details_students.html'


class DeleteStudentView(DeleteView):

    model = Student
    template_name = 'delete_student.html'
    success_url = reverse_lazy('homepage:students_list')


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
        return render(request, template_name=self.template_name,
                      context=context)

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


class JsonStudentView(View):

    def get(self, request):
        students = list(Student.objects.all().values())
        return JsonResponse(students, safe=False)


class CSVStudentView(View):

    def get(self, request):
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = "attachment; \
                filename=students_list.csv"
        writer = csv.writer(response)
        writer.writerow(["Name", "Book", "Subject"])
        students = Student.objects.all()
        for student in students:
            writer.writerow([
                student.name,
                student.book.name if student.book else None,
                student.subject.title if student.subject else None,
            ])
        return response


class SendMailView(View):

    def get(self, request):
        recipients = ['konstantin.dobro@gmail.com']
        send_email(title='123 title', description=' Just description',
                   recipients=recipients)

        return HttpResponse(f"Your message sent to {recipients}".
                            format(*recipients))
