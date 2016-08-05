from django import forms

from models import *
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'doej1234@chsknights.com'}))

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}),
            'password': forms.widgets.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}),
        }

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('mobile',)
        widgets = {
            'mobile': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
        }

class StudentProfileForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = ('student_id', 'grade_level')
        widgets = {
            'student_id': forms.TextInput(attrs={'class':'form-control', 'placeholder':'1100987654'}),
            'grade_level': forms.Select(attrs={'class':'form-control', 'placeholder':'Grade Level'}),
        }

class TeacherProfileForm(forms.ModelForm):

    class Meta:
        model = TeacherProfile
        fields = ('room',)
        widgets = {
            'room': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Room Number'}),
        }
