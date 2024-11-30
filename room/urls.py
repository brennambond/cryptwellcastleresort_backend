from django.urls import path

from . import api

urlpatterns = [
    path('', api.rooms_list, name='api_rooms_list'),
    path('<uuid:pk>/', api.rooms_detail, name='api_rooms_detail'),
    path('<uuid:pk>/book/', api.book_room, name='api_book_room'),
    path('<uuid:pk>/reservations/',
         api.room_reservations, name='api_room_reservations'),
    path('wings/', api.wings_list, name='api_wings_list'),
    path('wings/<uuid:pk>/', api.wings_detail, name='api_wings_detail'),
    path('categories/', api.categories_list, name='api_categories_list'),
]
