from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppDetailsViewSet

# Create a router for your viewsets
router = DefaultRouter()
router.register(r'app-details', AppDetailsViewSet, basename='app-details')

# Define the urlpatterns for this package
urlpatterns = [
    path('', include(router.urls)),  # Includes all routes registered in the router
]