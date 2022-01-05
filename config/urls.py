"""Main URLs module."""

from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),
    path('', include(('cride.circles.urls', 'circles'), namespace='circles')),
    path('', include(('cride.users.urls', 'users'), namespace='users')),
    path('', include(('cride.rides.urls', 'rides'), namespace='rides')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
