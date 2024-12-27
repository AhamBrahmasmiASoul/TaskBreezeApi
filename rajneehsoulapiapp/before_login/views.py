from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import AppDetails
from .serializers import AppDetailsSerializer

# AppDetails ViewSet
class AppDetailsViewSet(viewsets.ModelViewSet):
    queryset = AppDetails.objects.all()
    serializer_class = AppDetailsSerializer

    def list(self, request, *args, **kwargs):
        """
        Override the list method to return a single object instead of a list.
        """
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "No AppDetails available."}, status=404)

        # Use the first object in the queryset
        instance = queryset.first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Override the create method to customize how a new AppDetails instance is created.
        """
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Override the update method to customize how an AppDetails instance is updated.
        """
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Override the destroy method to customize how an AppDetails instance is deleted.
        """
        return super().destroy(request, *args, **kwargs)

    # Optionally, add custom actions (e.g., for retrieving a specific related field)
    @action(detail=True, methods=['get'])
    def get_app_specific_details(self, request, pk=None):
        app_details = self.get_object()
        return Response({
            'appSpecificDetails': app_details.app_specific_details
        })
