from django.urls import path

from . import views

urlpatterns = [
    path('event/add', views.timeline_event_insert, name='timelinejs-event-add'),
    path('ete_2013', views.timeline_ete_2013, name='timelinejs-ete-2013'),


    ]