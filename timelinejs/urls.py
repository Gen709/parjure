from django.urls import path

from . import views

urlpatterns = [
    path('test/', views.calendar_test, name='calendar-details'),
    path('<int:pk>', views.timeline_details, name='timelinejs-details'),
    path('delete/<int:timeline_id>', views.delete_timeline_step1, name='delete-timeline-step1'),

    path('event/add', views.timeline_event_insert, name='timelinejs-event-add'),
    path('event/title/add/text/<int:title_slide_id>', views.timeline_add_text_to_the_event_title_slide, name='add-text-to-the-event-title-slide'),
    path('event/title/update/text/<int:text_title_slide_id>', views.timeline_update_text_to_the_event_title_slide, name='update-text-to-the-event-title-slide'),

    path('event/slide/add/<int:timeline_id>', views.timeline_event_slide_insert, name='add-new-slide-to-timeline-events'),
    path('event/slide/update/', views.slide_update, name='update-slide-event'),
    path('event/slide/update/<int:slide_id>', views.slide_update, name='update-slide-event'),
    path('event/slide/delete/<int:pk>', views.SlideDeleteView.as_view(), name='delete-slide'),

    path('event/slide/text/add/<int:parent_id>', views.add_text_to_event_slide, name='add-text-to-event-slide'),
    path('event/slide/text/update/<int:text_id>', views.update_text_of_event_slide, name='update-text-of-event-slide'),

    path('event/slide/media/add/<int:parent_id>', views.add_media_to_event_slide, name='add-media-to-event-slide'),
    path('event/slide/media/update/<int:media_id>', views.update_media_of_event_slide, name='update-media-of-event-slide'),
    path('event/slide/media/delete/<int:pk>', views.DeleteMedia.as_view(), name='delete-media'),


    path('data/json/<int:timeline_id>', views.timeline_js_json_data_view, name='timeline-js-data-json'),







    path('era/add/<int:timeline_id>', views.era_add, name='era-add'),
    path('era/update/<int:era_id>', views.era_update, name='era-update'),

    path('slide/add', views.timeline_slide_insert, name='timelinejs-slide-add'),

    path('slide/text/add/<int:slide_id>', views.timeline_slide_text_insert, name='timelinejs-slide-text-add'),

    path('media/add', views.timeline_media_insert, name='timelinejs-media-add'),
    path('media/add/<int:slide_id>', views.timeline_media_insert, name='timelinejs-media-add'),



    path('era/text/add/<int:era_id>', views.timeline_slide_text_insert, name='timelinejs-text-add'),

    path('list/', views.timeline_list, name='timelinejs-list'),

    path('ete_2013', views.timeline_details, name='timelinejs-ete-2013'),
]
