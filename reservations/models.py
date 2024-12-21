import uuid
from django.db import models
from room.models import Room
from django.conf import settings


class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='reservations')
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['room', 'check_in', 'check_out'],
                name='unique_reservation_per_room'
            )
        ]

    def __str__(self):
        return f"Reservation {self.id} by {self.user.email} for for {self.room.title} from {self.check_in} to {self.check_out}"
