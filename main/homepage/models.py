from django.db import models


class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    social_url = models.CharField(max_length=200, null=True, blank=True)
    surname = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=100, blank=True)
    birthday = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    is_active = models.CharField(max_length=100, null=True)
    normalized_name = models.CharField(max_length=100, null=True)

    subject = models.ForeignKey('homepage.Subject', on_delete=models.SET_NULL,
                                null=True)


class Subject(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
