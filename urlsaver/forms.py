from django import forms
from .models import UrlEntry
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UrlForm(forms.ModelForm):
    class Meta:
        model = UrlEntry
        exclude = ['user', 'visit_count', 'created_at', 'is_deleted', 'deleted_at']
        widgets = {
            'url': forms.Textarea(attrs={'rows': 2, 'placeholder': 'https://example.com'}),
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Google'}),
        }
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))