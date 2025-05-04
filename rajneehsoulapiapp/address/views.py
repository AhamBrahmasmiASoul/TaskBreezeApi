# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Address
from .serializers import AddressSerializer
from ..CustomAuthentication import CustomAuthentication


class AddressView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            address = Address.objects.filter(user_id=request.user.emailIdLinked_id).first()
            if address:
                serializer = AddressSerializer(address)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"detail": "No address found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        print("request.user.emailIdLinked_id: ", request.user.emailIdLinked_id)
        if serializer.is_valid():
            # Optional: force the user field to match the logged-in user
            serializer.save(user_id=request.user.emailIdLinked_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
