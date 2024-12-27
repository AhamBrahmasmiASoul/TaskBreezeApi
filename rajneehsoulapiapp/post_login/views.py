from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import PostLoginAppData
from .serializers import PostLoginAppDataSerializer
from ..CustomAuthentication import CustomAuthentication


class PostLoginViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = PostLoginAppData.objects.all()
    serializer_class = PostLoginAppDataSerializer
