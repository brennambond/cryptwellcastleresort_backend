from django.urls import path
from . import api

urlpatterns = [
    path('', api.list_user_reservations, name='list_user_reservations'),
    path('create/', api.create_reservation, name='create_reservation'),
]
