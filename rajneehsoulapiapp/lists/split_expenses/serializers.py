from decimal import Decimal

from rest_framework import serializers
from .models import Group, Collaborator

from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            'id',
            'eName',
            'eAmt',
            'eRawAmt',
            'eQty',
            'eQtyUnit',
            'eDescription',
            'eExpenseType',
            'addedByCollaboratorId',
            'expenseForCollaborator',
            'groupId',
            'created_on',
            'eCreationId'
        ]
        read_only_fields = ['id', 'created_on']


class CollaboratorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Collaborator model.
    Includes all relevant fields for API interaction.
    """
    expenses = serializers.SerializerMethodField()
    status = serializers.CharField(read_only=True)
    class Meta:
        model = Collaborator
        fields = [
            'id',
            'createdBy',
            'collabUserId',
            'collaboratorName',
            'groupId',
            'created_on',
            'isActive',
            'collabEmailId',
            'status',  # read-only
            'settle_modes',
            'settle_mediums',
            'requested_payment_qr_url',
            'redirect_upi_url',
            'expenses',
        ]

    def get_expenses(self, collaborator):
        group = collaborator.groupId
        collaborator_id = collaborator.id

        categorized_expenses = {
            "self": [],
            "lend": [],
            "owe": []
        }

        expenses = Expense.objects.filter(groupId=group).order_by('-created_on')

        for expense in expenses:
            if not expense.expenseForCollaborator:
                continue

            added_by_me = expense.addedByCollaboratorId.id == collaborator_id
            for_me = expense.expenseForCollaborator.id == collaborator_id

            serialized = ExpenseSerializer(expense).data

            if added_by_me and for_me:
                categorized_expenses["self"].append(serialized)
            elif added_by_me:
                categorized_expenses["lend"].append(serialized)
            elif for_me:
                categorized_expenses["owe"].append(serialized)

        return categorized_expenses


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for the Group model.
    Includes nested collaborators and creator reference.
    """
    collaborators = CollaboratorSerializer(many=True, read_only=True)
    createdBy = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'created_on',
            'createdBy',
            'collaborators'
        ]
