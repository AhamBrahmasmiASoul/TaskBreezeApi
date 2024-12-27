from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rajneehsoulapiapp.post_login.views import PostLoginViewSet

router = DefaultRouter()
router.register(r'getPostLoginDetails', PostLoginViewSet, basename='getPostLoginDetails')

urlpatterns = [
    path('', include(router.urls)),
]
