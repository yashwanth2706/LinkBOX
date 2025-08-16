from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('visit/<int:pk>/', views.visit_url, name='visit_url'),
    path('add/', views.add_url, name='add_url'),
    path('delete/<int:pk>/', views.delete_url, name='delete_url'),
    path('trash/', views.show_trash, name='show_trash'),
    path('trash_data/', views.trash_data, name='trash_data'),
    path('trash_delete/', views.trash_delete, name='trash_delete'),
    path('trash_recover/', views.trash_recover, name='trash_recover'),
    path('details/<int:url_id>/', views.get_url_details, name='get_url_details'),
    path('edit/<int:url_id>/', views.edit_url_view, name='edit_url_view'),
    path('delete-selected/', views.delete_selected, name='delete_selected'),
    path('activity-data/', views.activity_data, name='activity_data'),
]
