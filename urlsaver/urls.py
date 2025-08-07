from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexPage, name='index'),
    path('visit/<int:pk>/', views.visit_url, name='visit-url'),
    path('add-url/', views.add_url, name='add-url'),
    path('delete/<int:pk>/', views.delete_url, name='delete-url'),
    path('trash/', views.show_trash, name='show-trash'),
    path('trash-data/', views.trash_data, name='trash-data'),
    path('trash-delete/', views.trash_delete, name='trash-delete'),
    path('trash-recover/', views.trash_recover, name='trash-recover'),
]
