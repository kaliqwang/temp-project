from django import forms

from .models import *
from categories.models import *
from base.forms import category_form_field

class AnnouncementForm(forms.ModelForm):
    category = category_form_field

    class Meta:
        model = Announcement
        fields = ('title', 'category', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Add a short, clear title', 'required':'required', 'autofocus':'autofocus'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Announcement body goes here', 'rows':'4', 'required':'required'}),
        }
