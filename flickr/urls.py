from django.urls import path

from . import views

urlpatterns = [
    path('detail/<int:pk>/', views.FlickrPhotoDetailView.as_view(), name='flicker-detail-view'),
    path('update/<int:pk>', views.FlickrPhotoUpdateView.as_view(), name='flicker-update-view'),
    path('update_function/<int:pk>', views.flickr_update_view, name='flicker-update-function-view'),
    path('list/', views.FlickrPhotosListView.as_view(), name='flicker-list-view'),
    path('album/list/<int:album_id>/', views.FlickrAlbumPhotosListView.as_view(), name='flicker-album-view'),

    path('album/create/', views.AlbumCreateView.as_view(), name='album-create-view'),
    # path('album/create2/', views.album_create, name='album-create-view-2'),
    path('album/detail/<int:pk>', views.AlbumDetailView.as_view(), name='album-detail-view'),
    # path('album/list/', views.AlbumListView.as_view(), name='album-list-view'),
    path('album/update/<int:pk>', views.AlbumUpdateView.as_view(), name='album-update-view'),
    path('album/delete/<int:pk>', views.AlbumDeleteView.as_view(), name='album-delete-view'),

]
