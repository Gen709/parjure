from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponse
from .models import Era, Events, Slide, Media, Text
from .forms import EventsForm, EventsModelForm, SlideModelForm, TextModelForm, MediaModelForm

# Create your views here.

def timeline_ete_2013(request):
    data_dict={}
    data = JsonResponse(data_dict, safe=False)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def timeline_event_insert(request):
    # insert event and continue to insert slides
    if (request.method == "POST"):
        # insert event, return the event id
        return redirect('timelinejs-slide-add')
    # insert event and continue to insert era

    # insert event and stop

    event_form = EventsModelForm()
    context = {'event_form': event_form}
    return render(request, 'timelinejs/event_form.html', context)


def timeline_slide_insert(request, timeline_id=None):
    p=None
    # insert slide and add another
    if (request.method == "POST"):
        p = request.POST
        slide_form = SlideModelForm(request.POST.get("slide_form"))
    #     redirect to text or media or stop
        if "add_text" in request.POST:
            return redirect('timelinejs-text-add')
        elif "add_media" in request.POST:
            return redirect('timelinejs-media-add')

    slide_form = SlideModelForm()

    context = {'slide_form': slide_form, "p": p}
    return render(request, 'timelinejs/slide_form.html', context)


def timeline_text_insert(request, slide_id=None):
    # insert slide and add another
    if (request.method == "POST"):
        text_form = TextModelForm(request.POST.get("slide_form"))
        if "add_slide" in request.POST:
            return redirect('timelinejs-slide-add')
        elif "add_media" in request.POST:
            return redirect('timelinejs-media-add')

    text_form = TextModelForm()
    context = {'text_form': text_form}
    return render(request, 'timelinejs/text_form.html', context)


def timeline_media_insert(request, slide_id=None):
    # insert slide and add another
    if (request.method == "POST"):
        media_form = MediaModelForm(request.POST.get("slide_form"))
    #     redirect to text or media
    # insert slide and add an era

    # insert slide and stop
    media_form = MedaiModelForm()
    context = {'media_form': media_form }
    return render(request, 'timelinejs/media_form.html', context)