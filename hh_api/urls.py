from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('useraccount.urls')),
    path('admin/', admin.site.urls),
    path('api/rooms/', include('room.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
