from random import randint

from django.core.management.base import BaseCommand
from faker import Faker

from homepage.models import Student, Subject, Book


class Command(BaseCommand):

    books = ['Zach0tka', 'za4etko', 'zachechotko', 'zaCHETKO', 'zacheton']

    """
        Help command that generate books for each student and them to DB
        You can set amount of student to generate using argument
        '-a' or '--am'
    """

    help = 'Generate books for all student(s) to the DB using Faker'

    def handle(self, *args, **options):

        faker = Faker()

        students = Student.objects.all()

        for student in students:
            self.stdout.write('Start write book to students')
            a = faker.sentence(ext_word_list=self.books, nb_words=1)
            student.book = Book.objects.create(name=a)
            student.save()
            self.stdout.write('End write book to students')
