from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rajneehsoulapiapp.CustomAuthentication import CustomAuthentication
from rajneehsoulapiapp.schedule_list.models import ScheduleItemList
from rajneehsoulapiapp.schedule_list.serializers import ScheduleItemListSerializers

from rest_framework.views import APIView

# class CustomBaseAuthenticatedView(APIView):
#     """
#     Base view to handle token differentiation and user type logic.
#     """
#     authentication_classes = [CustomAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get_user_data(self, request):
#         """
#         Return the appropriate user type and related user identifier.
#         """
#         user = request.user
#
#
#         if hasattr(user, "google_auth_user_id"):  # Social user
#             return user, {"google_auth_user_id": user.id}
#         elif hasattr(user, "userMobileLinked_id"):  # Custom user
#             return user, {"user_id": user.userMobileLinked_id}
#         else:
#             raise ValueError("Unknown user type")
#
#     def filter_queryset(self, queryset, user_filter):
#         """
#         Filter the queryset based on user-specific filters.
#         """
#         return queryset.filter(**user_filter)
#
#
# class ScheduleItemView(CustomBaseAuthenticatedView):
#     def get(self, request, item_id=None):
#         user, user_filter = self.get_user_data(request)
#         if item_id:
#             user_filter["id"] = item_id
#         schedule_items = self.filter_queryset(ScheduleItemList.objects, user_filter)
#
#         if not schedule_items.exists():
#             return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = ScheduleItemListSerializers(schedule_items, many=True)
#         return Response({"data": serializer.data}, status=status.HTTP_200_OK)

# Utility function to get user_object
def get_user_object(request):
    user = request.user
    if "Bearer" not in request.headers.get("Authorization", ""):
        return user.userMobileLinked_id
    return user.id

# Mixin for user validation
class UserValidationMixin:
    @staticmethod
    def validate_user(request):
        user_object = get_user_object(request)
        if user_object is None:
            return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)
        return user_object

class ScheduleItemView(APIView, UserValidationMixin):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id=None):
        user_object = self.validate_user(request)
        if isinstance(user_object, Response):
            return user_object

        if item_id:
            schedule_items = ScheduleItemList.objects.filter(id=item_id, user_id=user_object)
            if not schedule_items.exists():
                return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ScheduleItemListSerializers(schedule_items, many=True)
        else:
            schedule_items = ScheduleItemList.objects.filter(user_id=user_object)
            serializer = ScheduleItemListSerializers(schedule_items, many=True)

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user_object = self.validate_user(request)
        if isinstance(user_object, Response):
            return user_object

        serializer = ScheduleItemListSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=user_object)
            return Response(
                {'message': "Your Scheduled Data Saved Successfully", 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, item_id=None):
        user_object = self.validate_user(request)
        if isinstance(user_object, Response):
            return user_object

        if not item_id:
            return Response({"error": "Provide item id"}, status=status.HTTP_400_BAD_REQUEST)

        schedule_item = get_object_or_404(ScheduleItemList, id=item_id, user_id=user_object)
        serializer = ScheduleItemListSerializers(schedule_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id=None):
        user_object = self.validate_user(request)
        if isinstance(user_object, Response):
            return user_object

        if not item_id:
            return Response({"error": "Provide item id"}, status=status.HTTP_400_BAD_REQUEST)

        schedule_item = get_object_or_404(ScheduleItemList, id=item_id, user_id=user_object)
        schedule_item.delete()

        remaining_items = ScheduleItemList.objects.filter(user_id=user_object)
        serializer = ScheduleItemListSerializers(remaining_items, many=True)
        return Response(
            {
                'message': "Scheduled item deleted successfully.",
                "remainingItems": serializer.data,
            },
            status=status.HTTP_200_OK
        )

