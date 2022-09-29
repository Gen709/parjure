from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from .models import Era, Events, Slide, Media, Text
from .forms import EventsForm, EventsModelForm

# Create your views here.

def timeline_ete_2013(request):
    data_dict={}
    data = JsonResponse(data_dict, safe=False)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def timeline_event_insert(request):

    event_form = EventsModelForm()
    context = {'event_form': event_form}
    return render(request, 'timelinejs/event_form.html', context)