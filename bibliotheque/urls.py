from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.get_full_tree, name='home'),
    path('<int:pk>', views.get_full_tree, name='home'),
    path('leaf/delete/<int:pk>', views.deleting_leaf_node, name="delete-leaf-node"),

    path('get_image_list/', views.get_image_list, name='get_image_list'),

    path('bibliotheque/documentitem/data/json/', views.ajax_return_item_object, name='documentitem-ajax-get'),

    path('bibliotheque/requete/text/get/', views.text_get, name='bibliotheque-text-get'),
    path('bibliotheque/requete/text/add/child/', views.add_as_child, name='add-as-child'),
    path('bibliotheque/requete/text/add/child/<int:parent_id>', views.add_as_child, name='add-as-child'),
    path('bibliotheque/requete/text/add/siblings/', views.add_as_sibling, name='add-as-sibling'),
    path('bibliotheque/requete/text/add/siblings/<int:parent_id>', views.add_as_sibling, name='add-as-sibling'),
    path('bibliotheque/requete/text/update/', views.text_update, name='bibliotheque-text-update'),
    path('bibliotheque/requete/text/update/<int:pk>', views.text_update, name='bibliotheque-text-update'),
    path('bibliotheque/requete/text/delete/<int:pk>', views.SectionDeleteModelView.as_view(), name='bibliotheque-section-delete'),

    path('bibliotheque/requete/hierarchy/', views.render_hierarchical_data, name='bibliotheque-hierarchy'),    

    path('bibliotheque/requete/add/section/', views.section_add, name='bibliotheque-section-add'),

    # path('bibliotheque/requete/add/allegation/<int:left_sibling_id>', views.document_allegation_add, name='bibliotheque-allegation-add'),
    # path('bibliotheque/requete/add/section/<int:parent_id>', views.document_item_text_add, name='bibliotheque-section-add-2'),

    path('bibliotheque/requete/add/counterpoint/', views.counterpoint_add, name='bibliotheque-counterpoint-add'),
    path('bibliotheque/requete/add/counterpoint/<int:pk>', views.counterpoint_add, name='bibliotheque-counterpoint-add'),

    path('bibliotheque/requete/add/allegation/', views.allegation_add, name='bibliotheque-allegation-add'),
    path('bibliotheque/requete/add/allegation/<int:pk>', views.allegation_add, name='bibliotheque-allegation-add'),

    
    path('bibliotheque/requete/allegation/<int:pk>', views.get_related, name='bibliotheque-requete-allegation'),

    path('bibliotheque/requete/add/timelinejs/', views.timelinejs_add, name='bibliotheque-timeline-add_'),

    path('bibliotheque/requete/', views.requete, name='hierarchy'),
    path('bibliotheque/rebuttal/<int:pk>', views.rebuttal, name='rebuttal'),

    

    
]