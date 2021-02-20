import csv
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, ListView, \
    UpdateView, DetailView
from django.views.generic.base import View
from django.conf import settings

from .models import Student
from .emails import send_email


class HomePageView(View):
    template_name = 'home.html'

    def get(self, request):
        """
        Return html page
        """
        return render(request, self.template_name)


class StudentListView(ListView):

    model = Student
    template_name = 'students_list.html'


class CreateStudentView(CreateView):
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
