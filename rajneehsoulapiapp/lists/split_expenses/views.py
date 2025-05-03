import random
import string
from decimal import Decimal, ROUND_DOWN

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rajneehsoulapiapp.CustomAuthentication import CustomAuthentication
from rajneehsoulapiapp.lists.split_expenses.serializers import GroupSerializer, CollaboratorSerializer
from rajneehsoulapiapp.login.models import EmailIdRegistration
from .models import Group, Collaborator, Expense, ExpenseType
from .serializers import ExpenseSerializer

class GroupAPIView(APIView):
    """
    Handles creation and retrieval of Groups for the authenticated user.
    """
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Fetches all groups where the user is a collaborator.
        Also resolves any pending invitations.
        """
        linked_user_id = request.user.emailIdLinked_id
        print("linked_user_id", linked_user_id)


        userEmailId = request.user.emailIdLinked.emailId

        print("userEmailId: ",userEmailId)

        # Resolve pending invitations
        pending_collaborators = Collaborator.objects.filter(
            collabEmailId=userEmailId
        )
        print("pending_collaborators", pending_collaborators)

        for pending in pending_collaborators:
            pending.collabUserId_id = linked_user_id
            pending.isActive = True
            pending.save()

        # Fetch groups associated with the user
        group_ids = Collaborator.objects.filter(
            collabUserId=linked_user_id
        ).values_list('groupId', flat=True)

        groups = Group.objects.filter(id__in=group_ids)
        serializer = GroupSerializer(groups, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Creates a new group and adds the current user as an active collaborator.
        """
        linked_user_id = request.user.emailIdLinked_id
        data = request.data.copy()
        data['createdBy_id'] = linked_user_id

        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            group = serializer.save(createdBy_id=linked_user_id)
            email_obj = get_object_or_404(EmailIdRegistration, id=linked_user_id)
            collaborator_name = (email_obj.emailId or "").split("@")[0] if email_obj.emailId else "User@"+linked_user_id

            Collaborator.objects.create(
                groupId=group,
                collaboratorName = collaborator_name,
                createdBy_id=linked_user_id,
                collabUserId_id=linked_user_id,
                isActive=True
            )

            # Fetch groups associated with the user
            group_ids = Collaborator.objects.filter(
                collabUserId=linked_user_id
            ).values_list('groupId', flat=True)

            groups = Group.objects.filter(id__in=group_ids)
            serializer = GroupSerializer(groups, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """
        Updates a group if the user is the creator.
        """
        group_id = request.query_params.get('group_id')

        if not group_id:
            return Response({"detail": "Group ID is required for patch."}, status=status.HTTP_400_BAD_REQUEST)

        linked_user_id = request.user.emailIdLinked_id
        group = get_object_or_404(Group, id=group_id)

        if group.createdBy_id != linked_user_id:
            return Response({"detail": "You do not have permission to update this group."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = GroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Deletes a group if the user is the creator.
        """
        group_id = request.query_params.get('group_id')

        if not group_id:
            return Response({"detail": "Group ID is required for delete."}, status=status.HTTP_400_BAD_REQUEST)

        linked_user_id = request.user.emailIdLinked_id
        group = get_object_or_404(Group, id=group_id)

        if group.createdBy_id != linked_user_id:
            return Response({"detail": "You do not have permission to delete this group."},
                            status=status.HTTP_403_FORBIDDEN)

        group.delete()
        return Response({"detail": "Group deleted successfully."}, status=status.HTTP_200_OK)


class CollaboratorAPIView(APIView):
    """
    Handles collaborators - listing and adding them to groups.
    """
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Fetches collaborators for a given group, or all created by the user.
        """
        group_id = request.query_params.get('groupId')

        if group_id:
            collaborators = Collaborator.objects.filter(groupId_id=group_id)
        else:
            collaborators = Collaborator.objects.filter(createdBy=request.user)

        serializer = CollaboratorSerializer(collaborators, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Adds a collaborator to a group, with a pending invitation
        if the user is not registered.
        """
        data = request.data.copy()
        email = data.get('emailId')
        group_id = data.get('groupId')
        linked_user_id = request.user.emailIdLinked_id

        if not email or not group_id:
            return Response(
                {"detail": "emailId and groupId are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        data.update({
            'createdBy': linked_user_id,
            'collabEmailId': email,
            'isActive': False
        })

        try:
            user = EmailIdRegistration.objects.get(emailId=email)
            data['collabUserId'] = user.id
        except EmailIdRegistration.DoesNotExist:
            data['collabUserId'] = None  # Will remain a pending invitation

        serializer = CollaboratorSerializer(data=data)
        if serializer.is_valid():
            collaborator = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """
        Partially updates a collaborator by ID.
        """
        linked_user_id = request.user.emailIdLinked_id

        collaborator_id = request.data.get('id')
        if not collaborator_id:
            return Response({"detail": "Collaborator ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        collaborator = get_object_or_404(Collaborator, id=collaborator_id)
        print(f"collaborator : {collaborator}")
        print(f"collaborator.createdBy : {collaborator.createdBy_id}")
        print(f"collaborator.collabUserId : {collaborator.collabUserId_id}")
        print(f"linked_user_id : {linked_user_id}")
        # Optional: Only allow patch if the requesting user is creator
        if collaborator.collabUserId_id != linked_user_id:
            return Response({"detail": "You do not have permission to update this collaborator."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = CollaboratorSerializer(collaborator, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Deletes a collaborator by ID.
        """
        collaborator_id = request.query_params.get('id')
        linked_user_id = request.user.emailIdLinked_id

        if not collaborator_id:
            return Response({"detail": "Collaborator ID is required in query params."},
                            status=status.HTTP_400_BAD_REQUEST)

        collaborator = get_object_or_404(Collaborator, id=collaborator_id)

        # Optional: Only allow to delete if the requesting user is creator
        if collaborator.createdBy_id != linked_user_id:
            return Response({"detail": "You do not have permission to delete this collaborator."},
                            status=status.HTTP_403_FORBIDDEN)

        # Get all expenses related to this collaborator (if any) and delete them
        expenses = Expense.objects.filter(expenseForCollaborator=collaborator_id)
        if expenses.exists():
            e_creation_id = expenses.first().eCreationId
            all_related_expenses = Expense.objects.filter(eCreationId=e_creation_id)
            print("expenses: ", all_related_expenses)
            all_related_expenses.delete()

        collaborator.delete()
        return Response({"detail": "Collaborator deleted."}, status=status.HTTP_200_OK)


class ExpenseAPIView(APIView):

    def get(self, request):
        group_id = request.query_params.get('groupId')
        collab_id = request.query_params.get('collaboratorId')

        if not group_id or not collab_id:
            return Response({'error': 'groupId and collaboratorId are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = Group.objects.get(id=group_id)
            caller_collaborator = Collaborator.objects.get(id=collab_id, groupId=group)
        except (Group.DoesNotExist, Collaborator.DoesNotExist):
            return Response({'error': 'Group or Collaborator not found'}, status=status.HTTP_404_NOT_FOUND)

        expenses = Expense.objects.filter(groupId=group).order_by('-created_on')

        self_list = []
        lend_list = []
        owe_list = []

        for expense in expenses:
            if expense.expenseForCollaborator is None:
                continue  # safety check

            # SELF
            if expense.addedByCollaboratorId.id == caller_collaborator.id and expense.expenseForCollaborator.id == caller_collaborator.id:
                self_list.append(ExpenseSerializer(expense).data)

            # LEND
            elif expense.addedByCollaboratorId.id == caller_collaborator.id and expense.expenseForCollaborator.id != caller_collaborator.id:
                lend_list.append(ExpenseSerializer(expense).data)

            # OWE
            elif expense.addedByCollaboratorId.id != caller_collaborator.id and expense.expenseForCollaborator.id == caller_collaborator.id:
                owe_list.append(ExpenseSerializer(expense).data)

        return Response({
            "self": self_list,
            "lend": lend_list,
            "owe": owe_list
        }, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()

        try:
            group = Group.objects.get(id=data.get('groupId'))
            added_by = Collaborator.objects.get(id=data.get('addedByCollaboratorId'), groupId=group)
        except (Group.DoesNotExist, Collaborator.DoesNotExist):
            return Response({'error': 'Invalid group or collaborator'}, status=status.HTTP_400_BAD_REQUEST)

        expense_type = data.get('eExpenseType')
        e_raw_amt = data.get('eAmt')
        data["addedByCollaboratorId"] = added_by.id  # ensure consistency
        eCreationId = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        data["eCreationId"] = eCreationId
        data["eRawAmt"] = e_raw_amt

        if expense_type == "self":
            data["expenseForCollaborator"] = added_by.id
            return self._create_single_expense(data)

        elif expense_type in ["shared-equally", "custom-split"]:
            collaborators = Collaborator.objects.filter(groupId=group)
            return self._create_multiple_expenses(data, collaborators)

        return Response({'error': 'Invalid expense type'}, status=status.HTTP_400_BAD_REQUEST)

    def _create_single_expense(self, data):
        serializer = ExpenseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _create_multiple_expenses(self, base_data, collaborators):
        created_expenses = []
        total = collaborators.count()

        for collab in collaborators:
            entry = base_data.copy()
            entry["expenseForCollaborator"] = collab.id

            if base_data.get("eExpenseType") == "shared-equally":
                entry["eAmt"] = (Decimal(base_data["eAmt"]) / total).quantize(Decimal('.01'), rounding=ROUND_DOWN)

            serializer = ExpenseSerializer(data=entry)
            if serializer.is_valid():
                expense = serializer.save()
                created_expenses.append(ExpenseSerializer(expense).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(created_expenses, status=status.HTTP_201_CREATED)

    def patch(self, request, expense_id):
        expense = get_object_or_404(Expense, id=expense_id)
        serializer = ExpenseSerializer(expense, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, expense_id):
        expense = get_object_or_404(Expense, id=expense_id)
        expense.delete()
        return Response({"detail": "Expense deleted successfully."}, status=status.HTTP_200_OK)

