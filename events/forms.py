from django import forms

from .models import *
from categories.models import *
from base.forms import category_form_field

class EventForm(forms.ModelForm):
    category = category_form_field

    class Meta:
        model = Event
        fields = ('name', 'category', 'location', 'date_start', 'time_start', 'date_end', 'time_end', 'category', 'details')
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Add a short, clear name'}),
            'location': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Include a place or address'}),
            'date_start': forms.TextInput(attrs={'class':'form-control date start', 'placeholder':'mm/dd/yyyy'}),
            'time_start': forms.TextInput(attrs={'class':'form-control time start'}),
            'date_end': forms.TextInput(attrs={'class':'form-control date end', 'placeholder':'mm/dd/yyyy'}),
            'time_end': forms.TextInput(attrs={'class':'form-control time end'}),
            'details': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Tell people more about the event', 'rows':'4'}),
        }
