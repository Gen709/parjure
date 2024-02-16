def get_data_from_form(validated_django_form_obj):
    obj_dict = {}
    for key, value in validated_django_form_obj.cleaned_data.items():
        if value:
            obj_dict[key] = value
    return obj_dict