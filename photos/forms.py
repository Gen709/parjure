from django.forms import ModelForm
from django import forms

from .models import FlikrPhoto, Album


class FlikrPhotoModelForm(ModelForm):
    class Meta:
        model = FlikrPhoto
        fields = ['headline', 'text']

class FlikrPhotoAlbumModelForm(ModelForm):

    class Meta:
        model = Album
        fields = '__all__'

    photos = forms.ModelMultipleChoiceField(
        queryset=FlikrPhoto.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class FlikrPhotoAlbumNoPhotosModelForm(ModelForm):

    class Meta:
        model = Album
        exclude = ('photos',)