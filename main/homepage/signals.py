from django.db.models.signals import pre_delete, pre_save # noqa
from django.dispatch import receiver

import gender_guesser.detector as gender
from homepage.models import Student

detector = gender.Detector()


@receiver(pre_save, sender=Student)
def normalized_name(sender, instance, **kwargs):
    instance.normalized_name = instance.name.lower()


@receiver(pre_save, sender=Student)
def gendering_student(sender, instance, **kwargs):
    if detector.get_gender(instance.name.split(' ')[0]) == 'male':
        instance.sex = 'M'
    else:
        instance.sex = 'F'

# @receiver(pre_delete, sender=Student)
# def deny_removing(sender, instance, **kwargs):
#     raise NameError('Don`t delete it')
