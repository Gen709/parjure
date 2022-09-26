# from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from .models import PhotosLibrary

# Create your views here.


def get_json_pictures(request):
    photo_list = PhotosLibrary.objects.filter(date__range=["2013-01-01", "2013-12-31"])
    data_dict = {}
    # data_dict["title"] = {"text": { "headline": "Parjure <br/> Élise Ayoub", "text": "<p>Le 25 septembre,
    # Élise Ayoub a commis un parjure afin d'obtenir la garde exclusive de ses enfants.</p>" } }
    events = []
    for p in photo_list:
        events.append({'start_date': {'year': p.date.year,
                                      'month': p.date.month,
                                      'day': p.date.day,
                                      'hour': p.date.hour,
                                      'minute': p.date.minute,
                                      'second': p.date.second
                                      },
                       'media': {"url": "data/photos/" + p.file.path.split('/')[-1],
                                 "caption": "Caption of the picture"
                                 }
                       })

    data_dict["events"] = events
    data = JsonResponse(data_dict, safe=False)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
