from django.core.management.base import BaseCommand
from faker import Faker
from homepage.models import Student


class Command(BaseCommand):
    
    """
        Help command that generate studentsmodels and add them to DB
        By default generate 10 students.
        You can set amount of student to generate using argument
        '-a' or '--am' 
    """
    
    help = 'Generate and add new student(s) to the DB using Faker'

    def add_arguments(self, parser):
        parser.add_argument('-a', '--am', type=int, default=10)

    def handle(self, *args, **options):
        
        faker = Faker()

        self.stdout.write('Start generating and inserting Students')
        for _ in range(options['am']):
            self.stdout.write('Start inserting Students')
            student = Student()
            student.name = faker.name()
            student.save()
        self.stdout.write('End inserting Students')
