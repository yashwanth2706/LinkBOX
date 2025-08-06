from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexPage, name='index'),
    path('visit/<int:pk>/', views.visit_url, name='visit-url'),
]
