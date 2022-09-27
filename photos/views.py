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
                                 "caption": p.file.url,
                                 "group":p.group
                                 },
                       'text': {"headline":"",
                                "text":p.headline
                                }
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
    events.append({'start_date': {'year': 2013,
                                  'month': 5,
                                  'day': 5,
                                  },
                   'end_date': {'year': 2013,
                                'month': 5,
                                'day': 5,
                                },
                   'type': "era",
                   'text': {'headline': "Ile Ste-Hélène",
                            'text': "Le 5 mai 2013 le défendeur etait avec sa fille Alexia, acompagné de son amie Sandrine Corbin et de ses parents. Ils étaient au château de Raiponse (le chateau d'eau de l'ile Ste-Hélène) et y ont passé l'apré-midi pendant que la demanderesse etait chez elle avec Nicolas"}
                   })
    events.append({'start_date': {'year': 2013,
                                  'month': 5,
                                  'day': 17,
                                  },
                   'end_date': {'year': 2013,
                                'month': 5,
                                'day': 17,
                                },
                   'type': "era",
                   'text': {'headline': "Alexia, Sandrine et le parc Alexandra",
                            'text': "Le 17 mai, le défendeur accompagne les filles au parc Alexandra pendant que la demanderesse reste à la maison avec Nicolas"}
                   })
    data_dict["events"] = events
    data_dict["era"] = {"start_date": dt(2013, 5, 21),
                        "end_date": dt(2013, 11, 21),
                        "text": "bla bla"}
    data = JsonResponse(data_dict, safe=False)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
