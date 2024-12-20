from django.urls import path
from . import api

urlpatterns = [
    path('', api.list_user_reservations, name='list_user_reservations'),
    path('create/', api.create_reservation, name='create_reservation'),
    path('<uuid:reservation_id>/', api.get_reservation, name='get_reservation'),
    path('<uuid:reservation_id>/update/',
         api.update_reservation, name='update_reservation'),
    path('<uuid:reservation_id>/delete/',
         api.delete_reservation, name='delete_reservation'),
]
