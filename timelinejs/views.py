from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .models import Era, Events, Slide, Media, Text
from flickr.models import Flickr
from .forms import EventsModelForm, SlideModelForm, TextModelForm, MediaModelForm, EraModelForm

from functions import create_object, timeline_js, date_functions

from datetime import datetime as dt
# Create your views here.


def timeline_details(request, pk):
    timelinejs_qs = Events.objects.get(id=pk)
    context = {'timelinejs': timelinejs_qs}
    return render(request, 'timelinejs/timelinejs_details.html', context)


def timeline_js_json_data_view(request, timeline_id):
    timelinejs_obj = Events.objects.get(id=timeline_id)

    timelinejs_dict = {"events": timeline_js.get_events_list(timelinejs_obj),
                       "title": timeline_js.get_title_dict(timelinejs_obj),
                       "eras": timeline_js.get_eras_list(timelinejs_obj),
                       "scale": timelinejs_obj.scale
                       }

    data = JsonResponse(timelinejs_dict, safe=False)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def timeline_list(request):
    timelinejs_qs = Events.objects.all()
    context = {'timelinejs_qs': timelinejs_qs}
    return render(request, 'timelinejs/timelinejs_list.html', context)


def delete_timeline_step1(request, timeline_id):
    timeline_to_be_deleted = Events.objects.get(id=timeline_id)
    related_events = timeline_to_be_deleted.events.all()
    related_era = timeline_to_be_deleted.era.all()

    context = {"timeline_to_be_deleted": timeline_to_be_deleted,
               "related_events": related_events,
               "related_era": related_era
               }
    return render(request, 'timelinejs/timelinejs_delete_step1.html', context)


def timeline_event_insert(request):
    if request.method == "POST":
        # Save title slide for timeline
        if "add_text" in request.POST:
            form = SlideModelForm(request.POST)
            if form.is_valid():
                new_event_title_slide = Slide.objects.create(**create_object.get_data_from_form(form))
                Events.objects.create(title=new_event_title_slide)
                return redirect('add-text-to-the-event-title-slide', title_slide_id=new_event_title_slide.id)
            else:
                context = {'form_step_name': "Failed to create Slide",
                           'next_step_list': ["add_text"],
                           'form': form
                           }
                return render(request, 'timelinejs/general_form.html', context)

    form_step_name = "Create Event title Slide"
    form = SlideModelForm()
    context = {'form_step_name': form_step_name,
               'next_step_list': ["add_text"],
               'form': form,
               'form_action': 'timelinejs-event-add'
               }
    return render(request, 'timelinejs/general_form.html', context)


def timeline_add_text_to_the_event_title_slide(request, title_slide_id):
    if request.method == "POST":
        # get the event
        # Save title slide for timeline
        # if the title slide of the event exist
        # check if the form is valid
        form = TextModelForm(request.POST)
        if form.is_valid():
            # check if the object already exist in the db
            try:
                # YES -> return form to update
                text_obj = Slide.objects.get(id=title_slide_id).text
                text_obj.headline = request.POST.get("headline", "")
                text_obj.text = request.POST.get("text", "")
                text_obj.save()
                return redirect(text_obj.event_title.all()[0].get_absolute_url())

            except:
                #  NO ->
                # create text
                title_slide_text = Text.objects.create(**create_object.get_data_from_form(form))
                # get the slide
                title_slide = Slide.objects.get(id=title_slide_id)
                # associate the title slide with the text
                title_slide.text = title_slide_text
                # save the change
                title_slide.save()
                return redirect(title_slide.event_title.all()[0].get_absolute_url())
        #     get the slide

        else:
            form_step_name = "Add Text to Event title Slide (invalid form)"
            context = {'form_step_name': form_step_name,
                       'next_step_list': ["add new slide"],
                       'form': form,
                       'form_action': 'add-text-to-the-event-title-slide',
                       'argument': title_slide_id
                       }
            return render(request, 'timelinejs/general_form.html', context)

    form_step_name = "Add Text to Event title Slide"
    form = TextModelForm()
    context = {'form_step_name': form_step_name,
               'next_step_list': ["add new slide"],
               'form': form,
               'form_action': 'add-text-to-the-event-title-slide',
               'argument': title_slide_id
               }
    return render(request, 'timelinejs/general_form.html', context)


def timeline_update_text_to_the_event_title_slide(request, text_title_slide_id):
    if request.method == "POST":
        form = TextModelForm(request.POST)
        if form.is_valid():
            text_obj = Text.objects.get(id=text_title_slide_id)
            text_obj.headline = form.cleaned_data["headline"]
            text_obj.text = form.cleaned_data['text']
            text_obj.save()
            return redirect(text_obj.slide_set.all()[0].event_title.all()[0].get_absolute_url())

    form = TextModelForm(instance=Text.objects.get(id=text_title_slide_id))

    context = {'form_step_name': 'Update Slide Title text',
               'next_step_list': ["Update"],
               'form': form,
               'form_action': 'update-text-to-the-event-title-slide',
               'argument': text_title_slide_id
               }

    return render(request, 'timelinejs/general_form.html', context)


def timeline_event_slide_insert(request, timeline_id):
    event_obj = Events.objects.get(id=timeline_id)
    if request.method == "POST":
        slide_form = SlideModelForm(request.POST)
        if slide_form.is_valid():
            # create object
            slide_obj = Slide(**create_object.get_data_from_form(slide_form))
            # save object
            slide_obj.save()
            # get parent
            try:
                #  add object to parent
                event_obj.events.add(slide_obj)
                # save change
                event_obj.save()
                # redirect to add text to the slide
                if "add media" in request.POST:
                    return redirect('add-media-to-event-slide', parent_id=slide_obj.id)
                elif "add text" in request.POST:
                    return redirect('add-text-to-event-slide', parent_id=slide_obj.id)
                else:
                    pass
                # redirect to add media to the slide
            except:
                slide_obj.delete()
                return redirect(slide_obj.title_event_set.all[0].get_absolute_url())

    form = SlideModelForm()

    context = {'parent_obj': Events.objects.get(id=timeline_id),
               'form_step_name': 'Create a new Timeline Event',
               'next_step_list': ["add media", "add text"],
               'form': form,
               'form_action': 'add-new-slide-to-timeline-events',
               'argument': timeline_id
               }
    return render(request, 'timelinejs/general_form.html', context)


def add_text_to_event_slide(request, parent_id):
    if request.method == "POST":
        form = TextModelForm(request.POST)
        if form.is_valid():
            slide_obj = Slide.objects.get(id=parent_id)
            text_obj = Text.objects.create(**create_object.get_data_from_form(form))
            slide_obj.text = text_obj
            slide_obj.save()
            return redirect(slide_obj.events_set.all()[0].get_absolute_url())

    else:
        form = TextModelForm()
        context = {'parent_obj': Slide.objects.get(id=parent_id),
                   'form_step_name': 'Add step to an Event Slide',
                   'next_step_list': ["add media", "Return to timeline"],
                   'form': form,
                   'form_action': 'add-text-to-event-slide',
                   'argument': parent_id
                   }
        return render(request, 'timelinejs/general_form.html', context)


def add_media_to_event_slide(request, parent_id):
    if request.method == "POST":
        form = MediaModelForm(request.POST)
        if form.is_valid():
            # media_obj = Media.objects.create(**create_object.get_data_from_form(form))
            media_obj = form.save()
            slide_obj = Slide.objects.get(id=parent_id)
            slide_obj.media = media_obj
            slide_obj.save()
            return redirect(slide_obj.events_set.all()[0].get_absolute_url())
        else:
            context = {'parent_obj': Slide.objects.get(id=parent_id),
                       'form_step_name': 'Add Media to an Event Slide',
                       'next_step_list': ["add text", "Save media and return to timeline"],
                       'form': form,
                       'form_action': 'add-media-to-event-slide',
                       'argument': parent_id
                       }
            return render(request, 'timelinejs/general_form.html', context)
        # path = request.path
    else:
        form = MediaModelForm()
        context = {'parent_obj': Slide.objects.get(id=parent_id),
                   'form_step_name': 'Add Media to an Event Slide',
                   'next_step_list': ["add text", "Save media and return to timeline"],
                   'form': form,
                   'form_action': 'add-media-to-event-slide',
                   'argument': parent_id
                   }
        return render(request, 'timelinejs/general_form.html', context)


def update_media_of_event_slide(request, media_id):
    instance = Media.objects.get(id=media_id)
    if request.method == "POST":
        form = MediaModelForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(instance.slide_set.all()[0].events_set.all()[0].get_absolute_url())
        else:
            pass
    else:
        form = MediaModelForm(instance=instance)
        context = {'parent_obj': '',
                   'form_step_name': 'Update Media to an Event Slide',
                   'next_step_list': ["add text", "Update media and Return to timeline"],
                   'form': form,
                   'form_action': 'update-media-of-event-slide',
                   'argument': media_id
                   }
        return render(request, 'timelinejs/general_form.html', context)


class DeleteMedia(DeleteView):
    model = Media
    template_name = "timelinejs/media_confirm_delete.html"
    def get_success_url(self):
        return reverse_lazy('timelinejs-details', kwargs={'pk':self.object.slide_set.all()[0].events_set.all()[0].id})


def update_text_of_event_slide(request, text_id):
    instance = Text.objects.get(id=text_id)
    if request.method == "POST":
        form = TextModelForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(instance.slide_set.all()[0].events_set.all()[0].get_absolute_url())

    else:
        form = TextModelForm(instance=instance)
        context = {'parent_obj': '',
                   'form_step_name': 'Update Text to an Event Slide',
                   'next_step_list': ["add text", "Update text and Return to timeline"],
                   'form': form,
                   'form_action': 'update-text-of-event-slide',
                   'argument': text_id
                   }
        return render(request, 'timelinejs/general_form.html', context)


def timeline_slide_insert(request, event_id=None):
    # insert slide and add another
    if request.method == "POST":
        slide_form = SlideModelForm(request.POST)
        if slide_form.is_valid():
            # create object
            slide_obj = Slide(**create_object.get_data_from_form(slide_form))
            # save object
            slide_obj.save()
            # get parent
            try:
                event_obj = Events.objects.get(id=request.POST.get("parent_id"))
                #  add object to parent
                event_obj.events.add(slide_obj)
                # save change
                event_obj.save()
            except:
                slide_obj.delete()
                return redirect('timelinejs-ete-2013')

            slide_id = str(slide_obj.id)
            #           get the slide pk to add the text or the media
            if "add_text" in request.POST:
                return redirect('timelinejs-text-add', slide_id=slide_id)
            elif "add_media" in request.POST:
                return redirect('timelinejs-media-add', slide_id=slide_id)

    slide_form = SlideModelForm()

    if event_id:
        event = Events.objects.get(id=event_id)
    else:
        event = None
    context = {'slide_form': slide_form,
               'parent_id': event_id,
               'event': event}
    return render(request, 'timelinejs/slide_form.html', context)


def slide_update(request, slide_id=None):
    if request.method == "POST":
        s = Slide.objects.get(id=request.POST.get('slide_id', None))
        form = SlideModelForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect(s.events_set.all()[0].get_absolute_url()) # aller chercher le event lié par
    else:
        s = Slide.objects.get(id=slide_id)
        form = SlideModelForm(instance=s)
        context={'slide_form': form,
                 'slide_id': slide_id,
                 'slide': s
                 }
        return render(request, 'timelinejs/slide_update_form.html', context)


class SlideDeleteView(DeleteView):
    model = Slide
    template_name = "timelinejs/slide_confirm_delete.html"
    def get_success_url(self):
        return reverse_lazy('timelinejs-details', kwargs={'pk':self.object.events_set.all()[0].id})


def timeline_slide_text_insert(request, slide_id=None):
    # insert slide and add another
    if request.method == "POST":
        text_form = TextModelForm(request.POST)

        if text_form.is_valid():
            text_obj = Text(**create_object.get_data_from_form(text_form))
            text_obj.save()
            try:
                slide_obj = Slide.objects.get(id=slide_id)
                slide_obj.text = text_obj
                slide_obj.save()
                if "add_slide" in request.POST:
                    return redirect('timelinejs-slide-add')
                elif "add_media" in request.POST:
                    return redirect('timelinejs-media-add')

            except:
                text_obj.delete()
                text_form = text_form
                context = {'text_form': text_form,
                           'parent_id': slide_id}
                return render(request, 'timelinejs/text_form.html', context)
        else:
            context = {'text_form': text_form,
                       'parent_id': slide_id}
            return render(request, 'timelinejs/text_form.html', context)
        #     get the slide object
    text_form = TextModelForm()
    context = {'text_form': text_form,
               'parent_id': slide_id}
    return render(request, 'timelinejs/text_form.html', context)


def timeline_media_insert(request, slide_id=None):
    # insert slide and add another
    if request.method == "POST":
        media_form = MediaModelForm(request.POST.get("slide_form"))
        if media_form.is_valid():
            #  save object
            if "add_slide" in request.POST:
                return redirect('timelinejs-slide-add')
    # insert slide and add an era

    # insert slide and stop
    media_form = MediaModelForm()
    context = {'media_form': media_form}
    return render(request, 'timelinejs/media_form.html', context)


def era_add(request, timeline_id):
    event = Events.objects.get(id=timeline_id)
    if request.method == "POST":
        text_form = TextModelForm(request.POST)
        if text_form.is_valid():
            t = text_form.save()
            era_form = EraModelForm(request.POST)
            # era_form.text = t
            if era_form.is_valid():
                e = era_form.save(commit=False)
                e.text = t
                e.save()
                event.era.add(e)
                return redirect(event.get_absolute_url())



    else:
        era_form = EraModelForm()
        text_form = TextModelForm()
        context = {'era_form': era_form,
                   'text_form': text_form,
                   'timeline_id': timeline_id
                   }
        return render(request, 'timelinejs/era_form.html', context)


def era_update(request, event_id=None):
    # insert slide and add another
    if request.method == "POST":
        era_form = EraModelForm(request.POST.get("slide_form"))
        text_form = TextModelForm(request.POST.get("slide_form"))
    #     redirect to text or media
    # insert slide and add an era
    else:
        # insert slide and stop
        if event_id:
            e = Era.objects.get(id=event_id)
            era_form = EraModelForm(instance=e)
            text_form = TextModelForm(instance=e.text)
        else:
            era_form = EraModelForm()
            text_form = TextModelForm()
        context = {'era_form': era_form,
                   'text_form': text_form}
        return render(request, 'timelinejs/era_form.html', context)


def calendar_test(request):
    context={}
    return render(request, 'timelinejs/calendar.html', context)

def ajax_calandar_data(request):
    string = "pas disponible"
    # get the date I've stayed home
    message = Flickr.objects.filter(title__icontains=string).order_by('date_taken_obj')
    conge_lp_list = [{"timestamp": x.date_taken_obj.strftime("%Y-%m-%d"),
                      "type": "Maladie Défendeur",
                      "url": x.link_to_original_photo} for x in message]
    c = [x.date_taken_obj for x in message]
    d = {'Conge Maternité Alexia': {'sdate': dt(2009, 10, 6),
                                    'edate': dt(2010, 10, 6)
                                    },
         'Belle Mère': {'sdate': dt(2010, 10, 7),
                        'edate': dt(2011, 10, 7)
                        },
         'Fair game': {'sdate': dt(2011, 10, 8),
                       'edate': dt(2012, 12, 31)
                       },
         'Conge Maternité Nicolas': {'sdate': dt(2012, 1, 1),
                                     'edate': dt(2013, 1, 1)
                                     },
         'Fair game 2': {'sdate': dt(2013, 1, 2),
                       'edate': dt(2014, 6, 1)
                       },
         'Congé maladie 2014': {'sdate': dt(2014, 6, 2),
                                'edate': dt(2014, 12, 1)
                                },
         }
