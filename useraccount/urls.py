from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api

urlpatterns = [
    path('register/', api.register_user, name='register_user'),
    path('<uuid:pk>/', api.user_detail, name='user_detail'),
    path('login/', api.login_user, name='login_user'),
    path('logout/', api.logout_user, name='logout_user'),
    path('current/', api.get_current_user, name='get_current_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
