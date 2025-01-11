from rest_framework import serializers
from .models import ExpenseItem, CollaboratorDetail, GroupExpense


class ExpenseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseItem
        exclude = ["collaborator"]  # Exclude the collab_user field

class CollaboratorDetailSerializer(serializers.ModelSerializer):
    expenses = ExpenseItemSerializer(many=True, read_only=True)  # Fetch related expenses

    class Meta:
        model = CollaboratorDetail
        fields = '__all__'


class GroupExpenseSerializer(serializers.ModelSerializer):
    collaborators = CollaboratorDetailSerializer(many=True, read_only=True)  # Fetch related collaborators

    class Meta:
        model = GroupExpense
        fields = '__all__'