import uuid

from django.conf import settings
from django.db import models

from useraccount.models import User


class Wing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='uploads/rooms')
    description = models.TextField()

    def __str__(self):
        return self.name

    def image_url(self):
        return f'{settings.WEBSITE_URL}{self.image.url}'


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
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    guests = models.IntegerField()
    category = models.ForeignKey(
        Category, related_name='category', on_delete=models.CASCADE)
    wing = models.ForeignKey(
        Wing, related_name='wing', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def image_url(self):
        return f'{settings.WEBSITE_URL}{self.image.url}'


class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(
        Room, related_name='reservations', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_nights = models.IntegerField()
    guests = models.IntegerField()
    total_price = models.FloatField()
    created_by = models.ForeignKey(
        User, related_name='reservations', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
