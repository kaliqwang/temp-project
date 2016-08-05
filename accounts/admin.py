from django.contrib import admin

from models import *
from django import forms

class CustomUserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

class CustomUserProfileAdminForm(forms.ModelForm):
    user = CustomUserChoiceField(queryset=User.objects.all())

    class Meta:
        model = UserProfile
        fields = ('user', 'mobile')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'mobile')

    form = CustomUserProfileAdminForm

    def get_full_name(self, obj):
        return obj
    get_full_name.short_description = 'name'
    get_full_name.admin_order_field = 'user__last_name'

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'student_id', 'grade_level')

class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'room')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(TeacherProfile, TeacherProfileAdmin)
