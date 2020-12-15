from django.db import models

# Create your models here.

class Student(models.Model):
    # Создать модель Student с полями(id, name, surname, age, sex, address, description, birthday, email)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    sex = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    birthday = models.CharField(max_length=100)
    email = models.CharField(max_length=100)