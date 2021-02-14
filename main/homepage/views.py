import csv
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic.base import View
from django.conf import settings

from .forms import StudentForm
from .models import Student


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
