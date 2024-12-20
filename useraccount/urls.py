from django.urls import path
from . import api

urlpatterns = [
    path('<uuid:pk>/', api.user_detail, name='user_detail'),
    path('register/', api.register_user, name='register_user'),
]
