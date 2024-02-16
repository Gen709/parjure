from django.urls import path

from . import views

urlpatterns = [
    path('timeline/json', views.get_json_pictures, name='timeline-json'),
    path('flikr', views.FlikrListView.as_view(), name='flikr-list'),
    path('flikr/detail/<int:pk>', views.flikerdetail, name='flikr-detail'),
    path('flikr/update/', views.fliker_update_view, name='flikr-detail'),
    path('album/create2/', views.album_create, name='album-create-view-2'),
    path('album/update/', views.AlbumUpdateView.as_view(), name='album-update-view'),
    # path('album/detail/', views.AlbumDetailView.as_view(), name='album-detail-view'),
    path('album/detail/<int:pk>', views.album_detail_view, name='album-detail-view'),
    path('album/delete/', views.AlbumDeleteView.as_view(), name='album-delete-view'),
    path('album/list/', views.AlbumListView.as_view(), name='album-list-view'),
    path('yearly-calendar/', views.yearly_calendar, name='yearly_calendar'),
    path('yearly-calendar-ajax/', views.YearlyCalendarView.as_view(), name='yearly_calendar_ajax'),

    ]

