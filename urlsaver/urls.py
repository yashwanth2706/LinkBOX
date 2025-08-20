from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm

urlpatterns = [
    # --- AUTHENTICATION URLS ---
    path('signup/', views.signup_view, name='signup'),

    # class-based LoginView
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=CustomAuthenticationForm
    ), name='login'),

    # class-based LogoutView
    path('logout/', auth_views.LogoutView.as_view(
        template_name='registration/logged_out.html'
    ), name='logout'),

    # --- APP URLS ---
    path('', views.index, name='index'),
    path('visit/<int:pk>/', views.visit_url, name='visit_url'),
    path('add/', views.add_url, name='add_url'),
    path('delete/<int:pk>/', views.delete_url, name='delete_url'),
    path('trash/', views.show_trash, name='show_trash'),
    path('trash_data/', views.trash_data, name='trash_data'),
    path('trash_delete/', views.trash_delete, name='trash_delete'),
    path('trash_recover/', views.trash_recover, name='trash_recover'),
    path('get_url_details/<int:url_id>/', views.get_url_details, name='get_url_details'),
    path('edit_url_view/<int:url_id>/', views.edit_url_view, name='edit_url_view'),
    path('delete-selected/', views.delete_selected, name='delete_selected'),
    path('activity-data/', views.activity_data, name='activity_data'),
    path("export/selected/csv/", views.export_selected_csv, name="export_selected_csv"),
    path("export/selected/pdf/", views.export_selected_pdf, name="export_selected_pdf"),
    path("export/all/csv/", views.export_all_csv, name="export_all_csv"),
    path("export/all/pdf/", views.export_all_pdf, name="export_all_pdf"),
]