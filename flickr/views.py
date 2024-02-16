from django.shortcuts import render
from django.views.generic import DetailView

from .models import Flickr
# Create your views here.

class FlickrDetailView(DetailView):
    model=Flickr