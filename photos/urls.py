from django.urls import path

from . import views

urlpatterns = [
    path('timeline/json', views.get_json_pictures, name='timeline-json'),

    ]