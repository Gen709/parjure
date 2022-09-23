from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_full_tree, name='home'),
    path('bibliotheque/text/update/', views.bibliotheque_text_update, name='bibliotheque-text-update'),
    
]