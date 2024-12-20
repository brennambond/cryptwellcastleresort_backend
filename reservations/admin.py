from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'start_date',
                    'end_date', 'created_at')
    list_filter = ('start_date', 'end_date', 'room')
    search_fields = ('user__email', 'room__title')
