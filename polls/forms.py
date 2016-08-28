from django import forms

from .models import *
from categories.models import *
from base.forms import category_form_field

class PollForm(forms.ModelForm):
    category = category_form_field

    class Meta:
        model = Poll
        fields = ('content', 'category')
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What is your favorite ice cream flavor?', 'required':'required', 'autofocus':'autofocus'}),
        }
