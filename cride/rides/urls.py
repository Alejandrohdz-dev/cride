"""rides URLs."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Local
from .views import rides as rides_views

router = DefaultRouter()

router.register(
    r'rides/(?P<slug_name>[-a-zA-Z0-0_]+)/rides',
    rides_views.RideViewSet,
    basename='ride'
)

urlpatterns = [
    path('', include(router.urls))
]

