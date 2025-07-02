import uuid
from django.db import models
from django.conf import settings
import os


class Wing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(
        upload_to='uploads/wings', default='uploads/default-wing.png', null=True, blank=True
    )

    def save(self, *args, **kwargs):
        # Don't manually build image_url anymore
        if self.image and self.image.name:
            self.image_url = self.image.url  # Keep it synced if you must keep the field
        else:
            self.image_url = None
        super().save(*args, **kwargs)

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
    image = models.ImageField(
        upload_to="uploads/rooms/", default="uploads/default-room.png")
    image_url = models.URLField(blank=True, null=True)
    wing = models.ForeignKey(
        Wing, on_delete=models.CASCADE, related_name='rooms')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        bucket_domain = os.getenv(
            "AWS_S3_CUSTOM_DOMAIN", "hauntedhotel-backend-bucket.s3.us-east-1.amazonaws.com"
        )
        print(f"Bucket Domain: {bucket_domain}")  # Debugging bucket domain

        if self.image and self.image.name:
            # Debugging image name
            print(
                f"Constructing image_url for {self.title}: {self.image.name}")
            self.image_url = f"https://{bucket_domain}/{self.image.name}"
        else:
            # Debugging missing image
            print(f"No image found for {self.title}, using None for image_url")
            self.image_url = None

        # Debugging final result
        print(f"Final image_url for {self.title}: {self.image_url}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
