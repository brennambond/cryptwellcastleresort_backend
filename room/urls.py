from django.urls import path
from . import api

urlpatterns = [
    path('rooms/', api.rooms_list, name='api_rooms_list'),
    path('rooms/<uuid:pk>/', api.room_detail, name='api_rooms_detail'),
    path('wings/', api.wings_list, name='api_wings_list'),
    path('wings/<uuid:pk>/', api.wing_detail, name='api_wings_detail'),
    path('categories/', api.categories_list, name='api_categories_list'),
]
