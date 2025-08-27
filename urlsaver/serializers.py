from rest_framework import serializers
from .models import UrlEntry

class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlEntry
        fields = '__all__'   # OR we can also list specific fields
