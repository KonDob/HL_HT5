from django.contrib import admin
from django.utils.html import format_html, mark_safe

from .models import Student


class StudentAdmin(admin.ModelAdmin):

    class Meta:
        model = Student

    list_display = ['email', 'full_name', 'birthday']

    def full_name(self, obj):
        if obj.social_url:
            return format_html("<a href={}>{} {}</a>",
                               mark_safe(obj.social_url),
                               obj.name, obj.surname)
        else:
            return obj.name + ' ' + obj.surname


admin.site.register(Student, StudentAdmin)
