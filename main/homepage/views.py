import csv
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.shortcuts import redirect, render

from django.views.generic import DetailView
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import *  # noqa
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.cache import cache_page
from django.conf import settings

from .forms import StudentForm, BookForm, SubjectForm, \
    TeacherForm, UserSignUpForm
from .models import Student, Book, Subject, Teacher
from .send_email import send_email


class SignUpView(View):

    def get(self, request):
        sign_up_form = UserSignUpForm()
        return render(request, 'sign_up.html', context={
            'form': sign_up_form
        })

    def post(self, request):
        sign_up_form = UserSignUpForm(request.POST)
        if sign_up_form.is_valid():
            user = sign_up_form.save()
            user.set_password(request.POST['password1'])
            user.is_active = False
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activate_url = "{}/{}/{}".format(
                "http://localhost:8000/activate",
                uid,
                default_token_generator.make_token(user=user)
            )
            send_email(recipient_list=[user.email],
                       activate_url=activate_url)

            return HttpResponse("Check your email list to activate account!")
        return HttpResponse("wrong data")


class SignInView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            auth_form = AuthenticationForm()
            return render(request, 'sign_in.html',
                          context={
                              'form': auth_form
                          })
        else:
            return HttpResponse('User already logined')

    def post(self, request):
        user = authenticate(request=request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('homepage:students_list')
        else:
            return HttpResponse('Wrong data to login')


class SignOutView(View):

    def get(self, request):
        logout(request)

        return redirect('homepage:students_list')


class ActivateView(View):

    def get(self, request, uid, token):

        user_id = force_bytes(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)

        if not user.is_active and default_token_generator.check_token(user,
                                                                      token):
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponse("Token checked")
        else:
            return HttpResponse("Your account activated")


class HomePageView(View):
    template_name = 'home.html'

    def get(self, request):
        """
        Return html page
        """
        return render(request, self.template_name)


@method_decorator(cache_page(settings.CACHE_TTL), name='dispatch')
class StudentListView(View):
    template_name = 'students_list.html'

    def get(self, request):
        """
        Show all students in template
        """

        students = Student.objects.all()
        cache_value = cache.get('student_list')
        if not cache_value:
            cache.set('student_list', students)

        return render(request, self.template_name, {'students': students})

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
