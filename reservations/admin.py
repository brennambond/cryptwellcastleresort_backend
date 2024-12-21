from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'check_in',
                    'check_out', 'guests', 'created_at')
    list_filter = ('check_in', 'check_out', 'room')
    search_fields = ('user__email', 'room__title')
