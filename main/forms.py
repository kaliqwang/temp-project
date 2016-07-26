from django import forms

from django.contrib.admin.widgets import AdminSplitDateTime

from django.contrib.auth.models import User
from models import *

# sample_event_details = """Unlimited ice cream tasting for only $10! Our 100+ delicious flavors include classics like Vanilla, Chocolate, and Rocky Road, as well as specialty flavors such as Egg Nog, Cinnamon, Coffee, Butterscotch, and Green Tea.
#
# Ice Cream will also be available for purchase (certain flavors only):
# - Cup (8 oz): $2
# - Quart (32 oz): $4
# - Gallon (128 oz): $8
#
# It will be cold, so bring a sweater or jacket!
# """

category_form_field = forms.ModelChoiceField(required=False, queryset=Category.objects.all(), empty_label='Everyone (default)', widget=forms.Select(attrs={'class': 'form-control'}))

class AnnouncementForm(forms.ModelForm):
    category = category_form_field

    class Meta:
        model = Announcement
        fields = ('title', 'category', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Add a short, clear title', 'required':'required'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Put the body of your announcement here', 'rows':'6', 'required':'required'}),
        }

class EventForm(forms.ModelForm):
    category = category_form_field

    class Meta:
        model = Event
        fields = ('name', 'category', 'location', 'date_start', 'time_start', 'date_end', 'time_end', 'category', 'details')
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Add a short, clear name'}),
            'location': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Include a place or address'}),
            'date_start': forms.TextInput(attrs={'class':'form-control date start', 'placeholder':'Date'}),
            'time_start': forms.TextInput(attrs={'class':'form-control time start', 'placeholder':'Time'}),
            'date_end': forms.TextInput(attrs={'class':'form-control date end', 'placeholder':'Date'}),
            'time_end': forms.TextInput(attrs={'class':'form-control time end', 'placeholder':'Time'}),
            'details': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Tell people more about the event', 'rows':'6'}),
        }

class PollForm(forms.ModelForm):
    category = category_form_field

    class Meta:
        model = Poll
        fields = ('content', 'category')
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What is your favorite ice cream flavor?', 'required':'required'}),
        }

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
