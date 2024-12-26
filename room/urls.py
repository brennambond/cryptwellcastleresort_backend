from django.urls import path
from . import api

urlpatterns = [
    path('rooms/', api.list_rooms, name='list_rooms'),
    path('rooms/<uuid:room_id>/', api.get_room_detail, name='get_room_detail'),
    path('rooms/<uuid:room_id>/reservations/',
         api.get_room_reservations, name='get_room_reservations'),
    path('wings/', api.list_wings, name='list_wings'),
    path('wings/<uuid:wing_id>/', api.get_wing_detail, name='get_wing_detail'),
]
