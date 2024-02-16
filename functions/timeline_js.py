from timelinejs.models import Media, Text


def translate_date_to_js_fomat(date):
    date_dict = {'year':date.year,
                 'month':date.month,
                 'day':date.day,
                 'hour':date.hour,
                 'minute':date.minute,
                 'second':date.second
                }
    return date_dict


def get_events_list(timelinejs_obj):
    event_list = []
    # for event in timelinejs_obj.events.all().order_by('start_date'):
    for event in timelinejs_obj.get_events():
        event_dict = {}
        for k,v in event.__dict__.items():
            if k not in ['_state', 'pk'] and v:
                if "date" in k:
                    event_dict[k] = translate_date_to_js_fomat(v)
                    print("---------", k, event_dict[k])
                elif k == "media_id":
                    event_dict["media"]={}
                    media = Media.objects.get(id=v)
                    for media_k, media_v in media.__dict__.items():
                        if media_k not in ['_state', 'pk'] and media_v:
                            event_dict["media"][media_k] = media_v
                elif k == "text_id":
                    text = Text.objects.get(id=v)
                    event_dict["text"] = {}
                    for text_k, text_v in text.__dict__.items():
                        if text_k not in ['_state', 'pk'] and text_v:
                            event_dict["text"][text_k] = text_v
                else:
                    event_dict[k] = v

        event_list.append(event_dict)

    return event_list


def get_title_dict(timelinejs_obj):
    title_dict = {}
    for k, v in timelinejs_obj.title.__dict__.items():
        if k not in ['_state', 'pk'] and v:
            if k == "text_id":
                text = Text.objects.get(id=v)
                title_dict["text"] = {}
                for text_k, text_v in text.__dict__.items():
                    if text_k not in ['_state', 'pk'] and text_v:
                        title_dict["text"][text_k] = text_v
            else:
                title_dict[k] = v

    return title_dict


def get_eras_list(timelinejs_obj):
    era_dict_list = []
    era_dict = {}
    return era_dict_list


