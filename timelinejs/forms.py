from django import forms
from django.forms import ModelForm
from .models import Events, Slide, Text, Media


class EventsForm(forms.Form):
    your_name = forms.CharField(label="Insert your name", max_length=100)

class EventsModelForm(ModelForm):
    class Meta:
        model = Events
        fields = ['title', 'scale']

class SlideModelForm(ModelForm):
    class Meta:
        model = Slide
        fields = ['start_date', 'end_date', 'group', 'display_date', 'background_color', 'autolink', 'unique_id']


class TextModelForm(ModelForm):
    class Meta:
        model = Text
        fields = '__all__'


class MediaModelForm(ModelForm):
    class Meta:
        model = Media
        fields = "__all__"