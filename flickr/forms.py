from django.forms import ModelForm
from django import forms

from .models import Flickr, Album


class FlickrModelForm(ModelForm):
    class Meta:
        model = Flickr
        fields = ['title', 'desc']

class FlickrAlbumModelForm(ModelForm):

    class Meta:
        model = Album
        fields = '__all__'

    photos = forms.ModelMultipleChoiceField(
        queryset=Flickr.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class FlickrAlbumNoPhotosModelForm(ModelForm):

    class Meta:
        model = Album
        exclude = ('photos',)

