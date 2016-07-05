from django import forms

from django.contrib.admin.widgets import AdminSplitDateTime

from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget

from django.contrib.auth.models import User
from models import Announcement, Event, Poll, Category, StudentProfile, TeacherProfile

class AnnouncementForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject...', 'required': 'required'}))
    category = forms.ModelChoiceField(required=False, queryset=Category.objects.all(), empty_label='General (default)', widget=forms.Select(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Content...', 'rows': '6', 'required': 'required'}))

    class Meta:
        model = Announcement
        fields = ('title', 'category', 'content')

class EventForm(forms.ModelForm):
    category = forms.ModelChoiceField(required=False, queryset=Category.objects.all(), empty_label='General (default)', widget=forms.Select(attrs={'class': 'form-control'}))
    details = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Event Details (Optional)', 'rows': '6'}))

    class Meta:
        model = Event
        fields = ('name', 'category', 'location', 'date_start', 'time_start', 'date_end', 'time_end', 'category', 'details')
        dateOptions = {
            # 'format': 'mm - dd - yy',
            'autoclose': False,
            'showMeridian': True,
            'clearBtn': False,
            'startDate': '01/01/16',
        }
        timeOptions = {
            # 'format': 'HH:ii P',
            'autoclose': False,
            'showMeridian': True,
            'clearBtn': False,
            'startDate': '01/01/16',
        }
        widgets = {
            'date_start': DateWidget(attrs={'id': 'date-start', 'placeholder': 'TBA (default)'}, bootstrap_version=3, options=dateOptions),
            'time_start': TimeWidget(attrs={'id': 'time-start', 'placeholder': 'TBA (default)'}, bootstrap_version=3, options=timeOptions),
            'date_end': DateWidget(attrs={'id': 'date-end', 'placeholder': 'TBA (default)'}, bootstrap_version=3, options=dateOptions),
            'time_end': TimeWidget(attrs={'id': 'time-end', 'placeholder': 'TBA (default)'}, bootstrap_version=3, options=timeOptions),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Centennial Graduation Ceremony'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TBA (default)'}),
        }

class PollForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What is your favorite ice cream flavor?'}))
    category = forms.ModelChoiceField(required=False, queryset=Category.objects.all(), empty_label='General (default)', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Poll
        fields = ('content', 'category')

class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}))

    class Meta:
        model = Category
        fields = ('name', 'color')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.widgets.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name')

class StudentProfileForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = ('student_id', 'grade_level')
