from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

class UrlEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
        """
        Returns the effective category of the URL entry.

        If the category is "others", returns the custom_category, otherwise
        returns the category.
        """
        return self.custom_category if self.category == "others" else self.category

    def is_expired(self):
        """
        Checks if the URL entry has expired.

        A URL entry is considered expired if it is marked as deleted and the
        deleted_at field is set. If the URL entry is not deleted or the
        deleted_at field is not set, it is not considered expired.

        The URL entry is considered expired if the current time is more than 30
        days after the deleted_at field. Otherwise, it is not expired.

        Returns True if the URL entry has expired, False otherwise.
        """
        if self.is_deleted and self.deleted_at:
            return timezone.now() > self.deleted_at + timedelta(days=30)
        return False

    def __str__(self):
       # Returns a string representation of the URL entry.
       # If the URL entry has a name, returns the name. Otherwise, returns the URL.
        return self.name or self.url

def restore_url(entry_id):
    """
    Restores a deleted URL entry to active status.

    Given an entry_id, looks up the corresponding UrlEntry and sets is_deleted to False
    and deleted_at to None if the UrlEntry is currently marked as deleted.
    """    
    url = UrlEntry.objects.get(id=entry_id)
    if url.is_deleted:
        url.is_deleted = False
        url.deleted_at = None
        url.save()

def purge_expired():
    """
    Purges expired URL entries from the database.

    A URL entry is considered expired if it has been marked as deleted for
    30 days or more. This function looks up all expired URL entries and
    deletes them from the database.
    """
    now = timezone.now()
    expired = UrlEntry.objects.filter(is_deleted=True, deleted_at__lt=now - timedelta(days=30))
    expired.delete()
