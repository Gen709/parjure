from django.urls import path

from . import views

urlpatterns = [
    path('meida/add', views.timeline_media_insert, name='timelinejs-media-add'),
    path('text/add', views.timeline_text_insert, name='timelinejs-text-add'),
    path('slide/add', views.timeline_slide_insert, name='timelinejs-slide-add'),
    path('event/add', views.timeline_event_insert, name='timelinejs-event-add'),
    path('ete_2013', views.timeline_ete_2013, name='timelinejs-ete-2013'),


    ]