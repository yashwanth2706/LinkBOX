from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('visit/<int:pk>/', views.visit_url, name='visit-url'),
    path('add-url/', views.add_url, name='add-url'),
    path('delete/<int:pk>/', views.delete_url, name='delete-url'),
    path('trash/', views.show_trash, name='show-trash'),
    path('trash-data/', views.trash_data, name='trash-data'),
    path('trash-delete/', views.trash_delete, name='trash-delete'),
    path('trash-recover/', views.trash_recover, name='trash-recover'),
    path('get-url-details/<int:url_id>/', views.get_url_details, name='get-url-details'),
    path('edit-url/<int:url_id>/', views.edit_url_view, name='edit-url'),
    path('delete-selected/', views.delete_selected, name='delete-selected'),
    path('activity-data/', views.activity_data, name='activity-data'),
]
