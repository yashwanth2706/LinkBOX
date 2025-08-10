from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from datetime import timedelta

class UrlEntry(models.Model):
    name = models.CharField(max_length=255, blank=True)
    url = models.URLField()
    category = models.CharField(max_length=100, null=True, blank=True)
    custom_category = models.CharField(max_length=100, blank=True)
    sub_category = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    visit_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def effective_category(self):
        return self.custom_category if self.category == "others" else self.category

    def is_expired(self):
        if self.is_deleted and self.deleted_at:
            return timezone.now() > self.deleted_at + timedelta(days=30)
        return False

    def __str__(self):
        return self.name or self.url


class UrlGroup(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def url_count(self):
        return self.urls.count()

    def __str__(self):
        return self.name


class UrlGroupEntry(models.Model):
    group = models.ForeignKey(UrlGroup, related_name='urls', on_delete=models.CASCADE)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.group.name} - {self.url}"

def restore_url(entry_id):
    url = UrlEntry.objects.get(id=entry_id)
    if url.is_deleted:
        url.is_deleted = False
        url.deleted_at = None
        url.save()

def purge_expired():
    now = timezone.now()
    expired = UrlEntry.objects.filter(is_deleted=True, deleted_at__lt=now - timedelta(days=30))
    expired.delete()
