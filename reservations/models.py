# Updated `reservations/models.py`
from django.db import models
from django.conf import settings
from django.apps import apps


class Reservation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations"
    )
    room = models.ForeignKey(
        'room.Room',  # Use the app name and model name as a string
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    guests = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reservation by {self.user.email} for {self.room.title}"
