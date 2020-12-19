from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import Student
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Student
        
    # fieldsets = [
    #     ('Full Name', {'fields' : ['name', 'surname']}),        
    #     ('Student Email', {'fields': ['email']}),
    #     ('Birthday', {'fields': ['birthday']}),
    # ]
    
    list_display = ['full_name', 'email', 'birthday']

    def full_name(self, obj):
        #TODO
        if obj.social_url:        
            return format_html("<a href={}>{} {}</a>",mark_safe(obj.social_url), obj.name, obj.surname)
        else:
            return obj.name + ' ' + obj.surname


admin.site.register(Student, StudentAdmin)