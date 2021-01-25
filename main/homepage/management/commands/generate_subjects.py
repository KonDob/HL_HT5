from random import randint

from django.core.management.base import BaseCommand
from faker import Faker

from homepage.models import Student, Subject, Book


class Command(BaseCommand):

    subjects = ['Python', 'HTML\CSS', 'JS', 'Java', 'GO']


    """
        Help command that generate subjects for each student and them to DB
    """

    help = 'Generate subject for all student(s) to the DB using Faker'


    def handle(self, *args, **options):

        faker = Faker()

        students = Student.objects.all()

        for student in students:
            self.stdout.write('Start write subject to students')
            a = faker.sentence(ext_word_list=self.subjects, nb_words=1)
            Subject.objects.create(title=a)
            student.subject = Subject.objects.get(id=student.id)
            student.save()
            self.stdout.write('End write subject to students')
