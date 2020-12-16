from django.db import models


class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    sex = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    birthday = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
