from django.urls import path
from . import views

urlpatterns = [
    path('reservations/', views.list_user_reservations,
         name='list_user_reservations'),
    path('reservations/<str:room_id>/book/',
         views.create_reservation, name='create_reservation'),
]
