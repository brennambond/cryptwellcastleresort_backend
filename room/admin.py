from django.contrib import admin

from .models import Room, Reservation, Wing, Category

admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Wing)
admin.site.register(Category)
