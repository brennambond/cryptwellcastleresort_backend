import uuid
from django.db import models
from django.conf import settings


class Wing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.ImageField(
        upload_to='uploads/wings', null=True, blank=True)

    def image_url_full(self):
        return f"{settings.WEBSITE_URL}{self.image_url.url}" if self.image_url else None

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.IntegerField()
    beds = models.PositiveIntegerField(default=1)
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    guests = models.PositiveIntegerField(default=1)
    image_url = models.ImageField(
        upload_to='uploads/rooms', null=True, blank=True)
    wing = models.ForeignKey(
        Wing, on_delete=models.CASCADE, related_name='rooms')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def image_url_full(self):
        return f"{settings.WEBSITE_URL}{self.image_url.url}" if self.image_url else None

    def __str__(self):
        return self.title
