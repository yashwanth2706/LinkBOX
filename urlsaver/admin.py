from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# First, we must unregister the default User admin.
admin.site.unregister(User)

# Define our new, custom User admin.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Customizes the User admin interface to be more informative and user-friendly.
    """
    
    # --- List View Customization ---
    # This controls what columns are displayed in the user list.
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'is_staff', 
        'date_joined'
    )
    
    # This adds a "Filter" sidebar to filter users by their status.
    list_filter = (
        'is_staff', 
        'is_superuser', 
        'is_active', 
        'groups'
    )
    
    # This adds a search bar to search for users.
    search_fields = (
        'username', 
        'first_name', 
        'last_name', 
        'email'
    )
    
    # This controls the default sorting order. A '-' prefix means descending.
    ordering = ('-date_joined',)

    # --- Edit View Customization ---
    # This organizes the fields on the user's "edit" page into logical sections.
    fieldsets = (
        # Section 1: User Profile Information
        ('Personal info', {'fields': ('username', 'password', 'first_name', 'last_name', 'email')}),
        
        # Section 2: Permissions
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        
        # Section 3: Important Dates
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )