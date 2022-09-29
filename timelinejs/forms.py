from django import forms
from django.forms import ModelForm
from .models import Events


class EventsForm(forms.Form):
    your_name = forms.CharField(label="Insert your name", max_length=100)
class EventsModelForm(ModelForm):
    class Meta:
        model = Events
        fields = ['title', 'scale']