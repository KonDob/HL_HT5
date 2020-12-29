from django.forms import ModelForm

from .models import Student


class StudentForm(ModelForm):

    class Meta:
        model = Student
        fields = ['name', 'surname', 'normalized_name', 'social_url', 'age',
                  'sex', 'address', 'birthday', 'email', 'description']
