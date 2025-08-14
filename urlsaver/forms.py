from django import forms
from .models import UrlEntry

# For URL form validation
class UrlForm(forms.ModelForm):
    class Meta:
        model = UrlEntry
        fields = ['url', 'name', 'category', 'custom_category', 'sub_category', 'tags']
        widgets = {
            'url': forms.Textarea(attrs={'rows': 2, 'placeholder': 'https://example.com'}),
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Google'}),
        }