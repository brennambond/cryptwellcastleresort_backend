from django.urls import path
from . import api

urlpatterns = [
    path('wings/', api.list_wings, name='list_wings'),
    path('rooms/', api.list_rooms, name='list_rooms'),
]
