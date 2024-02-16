from django import forms
from django.forms import ModelForm
from .models import Events, Slide, Text, Media, Era


class EventsModelForm(ModelForm):
    class Meta:
        model = Events
        fields = ['scale']


class SlideModelForm(ModelForm):
    class Meta:
        model = Slide
        fields = ['start_date', 'end_date', 'group', 'display_date', 'background_color', 'autolink', 'unique_id']
        # widgets = {'event_id': forms.HiddenInput()}


class TextModelForm(ModelForm):
    class Meta:
        model = Text
        fields = '__all__'


class MediaModelForm(ModelForm):
    class Meta:
        model = Media
        fields = "__all__"


class EraModelForm(ModelForm):
    class Meta:
        model = Era
        fields = ['start_date', 'end_date']