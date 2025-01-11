from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import GroupExpense, CollaboratorDetail, ExpenseItem
from .serializers import GroupExpenseSerializer, CollaboratorDetailSerializer, ExpenseItemSerializer
from ...CustomAuthentication import CustomAuthentication


class GroupExpenseView(APIView):
    authentication_classes = [CustomAuthentication]  # Use the custom authentication class
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id=None):
        user = request.user
        if not user:
            return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if "Bearer" not in request.headers["Authorization"]:
            user_object = user.userMobileLinked_id
        else:
            user_object = user.id
        

        if group_id:
            group = get_object_or_404(GroupExpense, id=group_id, created_by_user=user_object)
            serializer = GroupExpenseSerializer(group)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            groups = GroupExpense.objects.filter(created_by_user=user_object)
            serializer = GroupExpenseSerializer(groups, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        if not user:
            return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)

        if "Bearer" not in request.headers["Authorization"]:
            user_object = user.userMobileLinked_id
        else:
            user_object = user.id

        print("userObject: ", type(user_object))

        serializer = GroupExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by_user_id=user_object)
            return Response(
                {'message': "Group created successfully", 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, group_id=None):
        print("group-expense-patch"*10)
        user = request.user
        if not user:
            return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)

        if not group_id:
            return Response({"error": "Provide group id"}, status=status.HTTP_400_BAD_REQUEST)

        if "Bearer" not in request.headers["Authorization"]:
            user_object = user.userMobileLinked_id
        else:
            user_object = user.id

        group = get_object_or_404(GroupExpense, id=group_id, created_by_user_id=user_object)
        serializer = GroupExpenseSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print("saved"*100)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, group_id=None):
        user = request.user
        if not user:
            return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)

        if not group_id:
            return Response({"error": "Provide group id"}, status=status.HTTP_400_BAD_REQUEST)

        if "Bearer" not in request.headers["Authorization"]:
            user_object = user.userMobileLinked_id
        else:
            user_object = user.id

        group = get_object_or_404(GroupExpense, id=group_id, created_by_user=user_object)
        group.delete()
        return Response({'message': "Group deleted successfully"}, status=status.HTTP_200_OK)


class CollaboratorDetailView(APIView):
    authentication_classes = [CustomAuthentication]  # Use the custom authentication class
    permission_classes = [IsAuthenticated]

    def get(self, request, collaborator_id=None):
        user = request.user
        if not user:
            return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)

        if "Bearer" not in request.headers["Authorization"]:
            user_object = user.userMobileLinked_id
        else:
            user_object = user.id

        if collaborator_id:
            collaborator = get_object_or_404(CollaboratorDetail, id=collaborator_id)
            serializer = CollaboratorDetailSerializer(collaborator)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            collaborators = CollaboratorDetail.objects.filter(collab_user_id=user_object)
            serializer = CollaboratorDetailSerializer(collaborators, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        if not user:
            return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CollaboratorDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': "Collaborator added successfully", 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, collaborator_id=None):
        user = request.user

        if not user:
            return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)

        if not collaborator_id:
            return Response({"error": "Provide collaborator id"}, status=status.HTTP_400_BAD_REQUEST)

        collaborator = get_object_or_404(CollaboratorDetail, id=collaborator_id)
        serializer = CollaboratorDetailSerializer(collaborator, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, collaborator_id=None):
        user = request.user
        if not user:
            return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)

        if not collaborator_id:
            return Response({"error": "Provide collaborator id"}, status=status.HTTP_400_BAD_REQUEST)

        collaborator = get_object_or_404(CollaboratorDetail, id=collaborator_id)
        collaborator.delete()
        return Response({'message': "Collaborator removed successfully"}, status=status.HTTP_200_OK)


class ExpenseItemView(APIView):
    authentication_classes = [CustomAuthentication]  # Use the custom authentication class
    permission_classes = [IsAuthenticated]

    def get(self, request, expense_id=None):
        user = request.user

        collaborator_id = request.data.get("collaborator_id")

        if not user:
            return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)

        if expense_id:
            expense = get_object_or_404(ExpenseItem, id=expense_id, collaborator_id= collaborator_id)
            serializer = ExpenseItemSerializer(expense)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            expenses = ExpenseItem.objects.filter(collaborator_id=collaborator_id)
            serializer = ExpenseItemSerializer(expenses, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        if not user:
            return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ExpenseItemSerializer(data=request.data)
        if serializer.is_valid():
            collaborator_id = request.data.get("collaborator_id")
            collaborator = get_object_or_404(CollaboratorDetail, id=collaborator_id)
            serializer.save(collaborator_id=collaborator_id)
            return Response(
                {'message': "Expense added successfully", 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, expense_id=None):
        user = request.user
        if not user:
            return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)

        if not expense_id:
            return Response({"error": "Provide expense id"}, status=status.HTTP_400_BAD_REQUEST)

        if "Bearer" not in request.headers["Authorization"]:
            user_scheduled_object = user.userMobileLinked_id
        else:
            user_scheduled_object = user.id

        expense = get_object_or_404(ExpenseItem, id=expense_id, collaborator_id=user_scheduled_object)
        serializer = ExpenseItemSerializer(expense, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, expense_id=None):
        user = request.user
        if "Bearer" not in request.headers["Authorization"]:
            user_scheduled_object = user.userMobileLinked_id
        else:
            user_scheduled_object = user.id

        if not user:
            return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)

        if not expense_id:
            return Response({"error": "Provide expense id"}, status=status.HTTP_400_BAD_REQUEST)

        expense = get_object_or_404(ExpenseItem, id=expense_id, collaborator_id=user_scheduled_object)
        expense.delete()
        return Response({'message': "Expense deleted successfully"}, status=status.HTTP_200_OK)
