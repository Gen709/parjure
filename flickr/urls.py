from django.urls import path

from . import views

urlpatterns = [
    path('detail/<int:pk>', views.FlickrDetailView.as_view(), name='flicker-detail-view'),
]
