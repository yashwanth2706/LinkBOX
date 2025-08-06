from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexPage, name='index'),
    path('visit/<int:pk>/', views.visit_url, name='visit-url'),
    path('add-url/', views.add_url, name='add-url'),
    path('delete/<int:pk>/', views.delete_url, name='delete-url'),
    path('trash/', views.show_trash, name='show-trash'),
    path('trash-data/', views.trash_data, name='trash-data'),
]
