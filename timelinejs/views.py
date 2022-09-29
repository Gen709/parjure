from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from .models import Era, Events, Slide, Media, Text

# Create your views here.

def timeline_ete_2013(request):

    data_dict={}
    data = JsonResponse(data_dict, safe=False)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)