from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api

urlpatterns = [
    path('<uuid:pk>/', api.user_detail, name='user_detail'),
    path('auth/user/', api.get_current_user, name='get_current_user'),
    path('auth/login/', api.login_user, name='login_user'),
    path("auth/logout/", api.logout_user, name="logout"),
    path('auth/register/', api.register_user, name='register_user'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
