from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import GroupExpense, CollaboratorDetail, ExpenseItem
from .serializers import GroupExpenseSerializer, CollaboratorDetailSerializer, ExpenseItemSerializer
from ...CustomAuthentication import CustomAuthentication


def is_bearer(request):
    return "Bearer" in request.headers.get("Authorization", "")


def get_user_object(request):
    user = request.user
    if is_bearer:
        return user.id
    return user.emailIdLinked_id

# Mixin for user validation
class UserValidationMixin:
    @staticmethod
    def validate_user(request):
        user_object = get_user_object(request)
        if user_object is None:
            return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)
        return user_object


# GroupExpenseView
class GroupExpenseView(APIView, UserValidationMixin):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id=None):
        user_object = self.validate_user(request)
        if isinstance(user_object, Response):
            return user_object

        if group_id:
            if is_bearer(request):
                group = get_object_or_404(GroupExpense, id=group_id, created_by_google_auth_user=user_object)
            else:
                group = get_object_or_404(GroupExpense, id=group_id, created_by_user=user_object)

            serializer = GroupExpenseSerializer(group)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            if is_bearer(request):
                groups = GroupExpense.objects.filter(created_by_google_auth_user=user_object)
            else:
                groups = GroupExpense.objects.filter(created_by_user=user_object)

            serializer = GroupExpenseSerializer(groups, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user_object = self.validate_user(request)
        print(user_object)
        if isinstance(user_object, Response):
            return user_object

        serializer = GroupExpenseSerializer(data=request.data)
        if serializer.is_valid():
            if is_bearer(request):
                serializer.save(created_by_google_auth_user_id=user_object)
            else:
                serializer.save(created_by_user_id=user_object)

            all_data = GroupExpense.objects.all()
            all_data_serializer = GroupExpenseSerializer(all_data, many=True)

            return Response(
                {'message': "Group created successfully", 'data': all_data_serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, group_id=None):
        user_object = self.validate_user(request)
        if isinstance(user_object, Response):
            return user_object

        if not group_id:
            return Response({"error": "Provide group id"}, status=status.HTTP_400_BAD_REQUEST)
        if is_bearer(request):
            group = get_object_or_404(GroupExpense, id=group_id, created_by_google_auth_user=user_object)
        else:
            group = get_object_or_404(GroupExpense, id=group_id, created_by_user_id=user_object)

        serializer = GroupExpenseSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            all_data = GroupExpense.objects.all()
            all_data_serializer = GroupExpenseSerializer(all_data, many=True)
            return Response({'data': all_data_serializer.data}, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, group_id=None):
        user_object = self.validate_user(request)
        if isinstance(user_object, Response):
            return user_object

        if not group_id:
            return Response({"error": "Provide group id"}, status=status.HTTP_400_BAD_REQUEST)

        if is_bearer(request):
            group = get_object_or_404(GroupExpense, id=group_id, created_by_google_auth_user=user_object)
        else:
            group = get_object_or_404(GroupExpense, id=group_id, created_by_user=user_object)

        group.delete()

        all_data = GroupExpense.objects.all()
        all_data_serializer = GroupExpenseSerializer(all_data, many=True)

        return Response({'message': "Group deleted successfully", 'data': all_data_serializer.data}, status=status.HTTP_200_OK)


# CollaboratorDetailView
class CollaboratorDetailView(APIView, UserValidationMixin):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, collaborator_id=None):
        user_object = self.validate_user(request)
        if isinstance(user_object, Response):
            return user_object

        if collaborator_id:
            collaborator = get_object_or_404(CollaboratorDetail, id=collaborator_id)
            serializer = CollaboratorDetailSerializer(collaborator)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            print("user_object : ", user_object)
            if is_bearer(request):
                collaborators = CollaboratorDetail.objects.filter(collab_google_auth_user_id=user_object)
            else:
                collaborators = CollaboratorDetail.objects.filter(collab_user_id=user_object)
            serializer = CollaboratorDetailSerializer(collaborators, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user_object = self.validate_user(request)
        if isinstance(user_object, Response):
            return user_object

        serializer = CollaboratorDetailSerializer(data=request.data)
        if serializer.is_valid():
            if is_bearer(request):
                serializer.save(collab_google_auth_user_id=user_object)
            else:
                serializer.save(collab_user_id=user_object)

            all_data = CollaboratorDetail.objects.all()
            all_data_serializer = CollaboratorDetailSerializer(all_data, many=True)

            return Response(
                {'message': "Collaborator added successfully", 'data': all_data_serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, collaborator_id=None):
        user_object = self.validate_user(request)
        if isinstance(user_object, Response):
            return user_object

        if not collaborator_id:
            return Response({"error": "Provide collaborator id"}, status=status.HTTP_400_BAD_REQUEST)

        collaborator = get_object_or_404(CollaboratorDetail, id=collaborator_id)
        serializer = CollaboratorDetailSerializer(collaborator, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            all_data = CollaboratorDetail.objects.all()
            all_data_serializer = CollaboratorDetailSerializer(all_data, many=True)
            return Response({'data': all_data_serializer.data}, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, collaborator_id=None):
        user_object = self.validate_user(request)
        if isinstance(user_object, Response):
            return user_object

        if not collaborator_id:
            return Response({"error": "Provide collaborator id"}, status=status.HTTP_400_BAD_REQUEST)

        collaborator = get_object_or_404(CollaboratorDetail, id=collaborator_id)
        collaborator.delete()

        all_data = CollaboratorDetail.objects.all()
        all_data_serializer = CollaboratorDetailSerializer(all_data, many=True)

        return Response({'message': "Collaborator removed successfully", 'data': all_data_serializer.data}, status=status.HTTP_200_OK)


class ExpenseItemView(APIView, UserValidationMixin):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, expense_id=None):
        user_object = self.validate_user(request)
        if isinstance(user_object, Response):
            return user_object

        collaborator_id = request.query_params.get("collaborator_id")  # Retrieve collaborator_id from query parameters

        if expense_id:
            if is_bearer(request):
                expense = get_object_or_404(ExpenseItem, id=expense_id, collaborator_id= collaborator_id, created_by_google_auth_user=user_object)
            else:
                expense = get_object_or_404(ExpenseItem, id=expense_id, collaborator_id= collaborator_id, created_by_user=user_object)
            serializer = ExpenseItemSerializer(expense)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

        else:
            if is_bearer(request):
                expenses = ExpenseItem.objects.filter(collaborator_id=collaborator_id, created_by_google_auth_user=user_object)
            else:
                expenses = ExpenseItem.objects.filter(collaborator_id=collaborator_id, created_by_user=user_object)
            serializer = ExpenseItemSerializer(expenses, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user_object = self.validate_user(request)
        if isinstance(user_object, Response):
            return user_object

        collaborator_id = request.query_params.get("collaborator_id")  # Retrieve collaborator_id from query parameters

        if not collaborator_id:
            return Response({"error": "Provide collaborator_id as a query parameter"},
                            status=status.HTTP_400_BAD_REQUEST)
        # Fetch collaborator or return 404 if not found
        get_object_or_404(CollaboratorDetail, id=collaborator_id)

        serializer = ExpenseItemSerializer(data=request.data)
        if serializer.is_valid():
            if is_bearer(request):
                serializer.save(created_by_google_auth_user_id=user_object, collaborator_id=collaborator_id)
            else:
                serializer.save(created_by_user_id=user_object, collaborator_id=collaborator_id)

            all_data = ExpenseItem.objects.all()
            all_data_serializer = ExpenseItemSerializer(all_data, many=True)

            return Response(
                {'message': "Expense added successfully", 'data': all_data_serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, expense_id=None):
        user_object = self.validate_user(request)
        if isinstance(user_object, Response):
            return user_object

        if not expense_id:
            return Response({"error": "Provide expense id"}, status=status.HTTP_400_BAD_REQUEST)

        collaborator_id = request.query_params.get("collaborator_id")  # Retrieve collaborator_id from query parameters

        if not collaborator_id:
            return Response({"error": "Provide collaborator_id as a query parameter"},
                            status=status.HTTP_400_BAD_REQUEST)

        expense = get_object_or_404(ExpenseItem, id=expense_id, collaborator_id=collaborator_id)
        serializer = ExpenseItemSerializer(expense, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            all_data = ExpenseItem.objects.all()
            all_data_serializer = ExpenseItemSerializer(all_data, many=True)


            return Response({'data': all_data_serializer.data}, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, expense_id=None):
        user_object = self.validate_user(request)
        if isinstance(user_object, Response):
            return user_object

        if not expense_id:
            return Response({"error": "Provide expense id"}, status=status.HTTP_400_BAD_REQUEST)

        collaborator_id = request.query_params.get("collaborator_id")  # Retrieve collaborator_id from query parameters

        if not collaborator_id:
            return Response({"error": "Provide collaborator_id as a query parameter"},
                            status=status.HTTP_400_BAD_REQUEST)

        expense = get_object_or_404(ExpenseItem, id=expense_id, collaborator_id=collaborator_id)
        expense.delete()

        all_data = ExpenseItem.objects.all()
        all_data_serializer = ExpenseItemSerializer(all_data, many=True)

        return Response({'message': "Expense deleted successfully",
                         'data': all_data_serializer.data}, status=status.HTTP_200_OK)
