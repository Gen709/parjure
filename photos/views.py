# from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.db.models import Count
from django.core.serializers import serialize
from django.utils import timezone
from .forms import FlikrPhotoAlbumModelForm, FlikrPhotoAlbumNoPhotosModelForm, FlikrPhotoModelForm
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .models import PhotosLibrary, TimelineEra, FlikrPhoto, Album

from django.urls import reverse
# from .models import MyModel

def get_json_pictures(request):
    photo_list = PhotosLibrary.objects.filter(date__range=["2013-05-01", "2013-09-21"])
    data_dict = {}
    events = []
    for p in photo_list:
        if p.caption:
            caption = ": " + p.caption
        else:
            caption = ""
        # if p.headline:
        #     headline=p.headline
        # else:
        #     headline=""

        events.append({'start_date': {'year': p.date.year,
                                      'month': p.date.month,
                                      'day': p.date.day,
                                      'hour': p.date.hour,
                                      'minute': p.date.minute,
                                      'second': p.date.second
                                      },
                       'media': {"url": p.file.url,
                                 "caption": p.date,
                                 "group": p.group
                                 },
                       'text': {"headline":"",
                                "text": p.headline
                                }
                       })
    for e in TimelineEra.objects.filter(start_date__range=["2013-05-01", "2013-09-21"]):
        events.append({'start_date': {'year': e.start_date.year,
                                      'month': e.start_date.month,
                                      'day': e.start_date.day,
                                      },
                       'end_date': {'year': e.end_date.year,
                                      'month': e.end_date.month,
                                      'day': e.end_date.day,
                                      },
                        'type': "era",
                        'text':{'headline': e.text_headline,
                                'text': e.text_text}
                       })
    # data_dict["title"]={"headline":"Été 2013",
    #                     "text": "En 2013, le défendeur est parti tout l'été et a laissé la demanderesse seule avec les deux (2) enfants"
    #                     }
    data_dict["events"] = events

    data = JsonResponse(data_dict, safe=False)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


class FlikrListView(ListView):
    model = FlikrPhoto
    template_name = 'photos/flikr_photo_list.html'  # Create this template
    context_object_name = 'flikr_photo_list'


def fliker_update_view(request):
    if request.method == "POST":
        # print("*****************", request.POST.get('inputName'))
        id = request.POST.get('picture_id')
        attribute = request.POST.get('inputName')
        value = request.POST.get("updated_value")
        photo = FlikrPhoto.objects.get(id=id)
        serie = photo.serie
        # synch all picture from the same serie
        for photo in FlikrPhoto.objects.filter(serie=serie):
            setattr(photo, attribute, value)
            photo.save()


    return HttpResponseRedirect(reverse('flikr-list'))


class FlikrDetailView(DetailView):
    model = FlikrPhoto
    template_name = 'photos/flikr_ detail.html'
    context_object_name = 'image'

    def get_queryset(self):
        thumbnail = FlikrPhoto.objects.get(pk=self.kwargs['pk'])
        print("*****************", thumbnail.serie)
        # Customize the queryset based on your needs
        queryset = FlikrPhoto.objects.filter(serie=thumbnail.serie, label='Original')
        return queryset


def flikerdetail(request, pk):
    # pk = request.GET.get("pk", )
    thumbnail = FlikrPhoto.objects.get(id=pk)
    print("*****************", thumbnail.serie)
    context = {'image': FlikrPhoto.objects.filter(serie=thumbnail.serie, label='Original').first()}
    return render(request, 'photos/flikr_ detail.html', context)


def album_create(request):
    if request.method == "POST":
        # request.POST._mutable = True
        form = FlikrPhotoAlbumModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('album-list-view')
        else:
            selected_photos = request.POST.get("photos")
            photos = FlikrPhoto.objects.all().order_by('date_taken')
            form = FlikrPhotoAlbumNoPhotosModelForm(request.POST)
            context={'selected_photos': selected_photos,
                     'photos': photos,
                     'form': form
                     }
            return render(request, 'photos/album_create_form.html', context)
    else:
        photos = FlikrPhoto.objects.filter(label="Thumbnail").order_by('date_taken')
        form = FlikrPhotoAlbumNoPhotosModelForm()
        context={'form': form, 'photos': photos}
        return render(request, 'photos/album_create_form.html', context)


class AlbumListView(ListView):
    model = Album
    template_name = 'photos/album_list.html'  # Create this template
    context_object_name = 'albums'


class AlbumUpdateView(UpdateView):
    model = Album
    template_name = 'photos/album_update.html'  # Create this template
    context_object_name = 'albums'


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'photos/album_detail.html'  # Create this template
    context_object_name = 'albums'


class AlbumDeleteView(DeleteView):
    model = Album
    template_name = 'photos/album_detail.html'  # Create this template
    context_object_name = 'albums'


def yearly_calendar(request):
    return render(request, 'photos/your_template.html')


class YearlyCalendarView(View):
    def get(self, request, *args, **kwargs):
        try:
            # Fetch details including URL for each date_taken
            photos = FlikrPhoto.objects.filter(label="Thumbnail")

            # Generate events based on unique date_taken values
            events = []
            for photo in photos:
                event = {
                    'id': str(photo.date_taken),
                    'title': f'{photo.headline[:15]}',
                    'url': photo.get_absolute_url(),
                    'start': photo.date_taken.strftime('%Y-%m-%d'),
                }
                
                if "email absence travail" in [x.name for x in photo.album_set.all()]:
                    event["backgroundColor"] = "red"

                events.append(event)

            return JsonResponse({'events': events}, safe=False)

        except Exception as e:
            # Handle other errors
            return JsonResponse({'error': str(e)}, status=500)


def album_detail_view(request, pk):
    album = get_object_or_404(Album, pk=pk)
    photos = album.photos.all()
    context = {'album': album, 'photos': photos}
    return render(request, 'photos/album_detail.html', context)
