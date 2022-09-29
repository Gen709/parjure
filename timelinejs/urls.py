from django.urls import path

from . import views

urlpatterns = [
    path('timelinejs/ete_2013', views.timeline_ete_2013, name='timelinejs-ete-2013'),

    ]