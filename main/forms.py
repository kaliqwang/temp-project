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

sample_event_details = "Tell people more about the event"

category_form_field = forms.ModelChoiceField(required=False, queryset=Category.objects.all(), empty_label='Everyone (default)', widget=forms.Select(attrs={'class': 'form-control'}))

class AnnouncementForm(forms.ModelForm):
    category = category_form_field

    class Meta:
        model = Announcement
        fields = ('title', 'category', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title...', 'required':'required', 'title':'Title', 'data-toggle':'tooltip', 'data-placement':'top', 'data-trigger':'focus'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Content...', 'required':'required', 'rows':'6', 'title':'Content', 'data-toggle':'tooltip', 'data-placement':'top', 'data-trigger':'focus'})
        }

class EventForm(forms.ModelForm):
    category = category_form_field

    class Meta:
        model = Event
        fields = ('name', 'category', 'location', 'date_start', 'time_start', 'date_end', 'time_end', 'category', 'details')
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Add a short, clear name', 'title':'Name', 'data-toggle':'tooltip', 'data-placement':'top', 'data-trigger':'focus'}),
            'location': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Include a place or address', 'title':'Location (Optional)', 'data-toggle':'tooltip', 'data-placement':'top', 'data-trigger':'focus'}),
            'date_start': forms.TextInput(attrs={'id':'date-start', 'class':'form-control date start', 'title':'Start', 'data-toggle':'tooltip', 'data-placement':'left', 'data-trigger':'focus', 'required':'required'}),
            'time_start': forms.TextInput(attrs={'id':'time-start', 'class':'form-control time start', 'title':'Start', 'data-toggle':'tooltip', 'data-placement':'left', 'data-trigger':'focus'}),
            'date_end': forms.TextInput(attrs={'id':'date-end', 'class':'form-control date end', 'title':'End', 'data-toggle':'tooltip', 'data-placement':'right', 'data-trigger':'focus'}),
            'time_end': forms.TextInput(attrs={'id':'time-end', 'class':'form-control time end', 'title':'End', 'data-toggle':'tooltip', 'data-placement':'right', 'data-trigger':'focus'}),
            'details': forms.Textarea(attrs={'class':'form-control', 'placeholder':sample_event_details, 'rows':'3', 'title':'Details (optional)', 'data-toggle':'tooltip', 'data-placement':'top', 'data-trigger':'focus'})
        }

class PollForm(forms.ModelForm):
    category = category_form_field

    class Meta:
        model = Poll
        fields = ('content', 'category')
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What is your favorite ice cream flavor?', 'required':'required'})
        }

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name', 'color')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'})
        }

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username', 'required':'required'}),
            'password': forms.widgets.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password', 'required':'required'}),
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name', 'required':'required'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name', 'required':'required'}),
            'email': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email (doej1234@chsknights.com)', 'required':'required'}),
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
            'student_id': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Student ID (Ex. 1100987654)', 'required':'required'}),
            'grade_level': forms.Select(attrs={'class':'form-control', 'placeholder':'Grade Level', 'required':'required'}),
        }
