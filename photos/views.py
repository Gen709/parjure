# from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from .models import PhotosLibrary

from datetime import datetime as dt

# Create your views here.


def get_json_pictures(request):
    photo_list = PhotosLibrary.objects.filter(date__range=["2013-05-01", "2013-09-21"])
    data_dict = {}
    # data_dict["title"] = {"text": { "headline": "Parjure <br/> Élise Ayoub", "text": "<p>Le 25 septembre,
    # Élise Ayoub a commis un parjure afin d'obtenir la garde exclusive de ses enfants.</p>" } }
    events = []
    for p in photo_list:
        if p.caption:
            caption=": "+p.caption
        else:
            caption=""
        events.append({'start_date': {'year': p.date.year,
                                      'month': p.date.month,
                                      'day': p.date.day,
                                      'hour': p.date.hour,
                                      'minute': p.date.minute,
                                      'second': p.date.second
                                      },
                       'media': {"url": p.file.url,
                                 "caption": dt.strftime(p.date, "%Y-%m-%d")+caption,
                                 "group":dt.strftime(p.date, "%Y-%m-%d")},
                       'text': {"headline": "",
                                "text":""}
                       })

    events.append({'start_date': {'year': 2013,
                                  'month': 5,
                                  'day': 1,
                                  },
                   'end_date': {'year': 2013,
                                   'month': 9,
                                   'day': 21,
                                   },
                    'type': "era",
                    'text':{'headline':"ETE 2013",
                            'text': "En 2013, le défendeur est parti tout l'été et a laissé la demanderesse seule avec les deux (2) enfants"}
                   })
    data_dict["events"] = events
    data_dict["era"] = {"start_date": dt(2013, 5, 21),
                        "end_date": dt(2013, 11, 21),
                        "text": "bla bla"}
    data = JsonResponse(data_dict, safe=False)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
