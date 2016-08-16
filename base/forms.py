from django import forms

from ..categories.models import *

category_form_field = forms.ModelChoiceField(required=False, queryset=Category.objects.all(), empty_label='Everyone (default)', widget=forms.Select(attrs={'class': 'form-control'}))
