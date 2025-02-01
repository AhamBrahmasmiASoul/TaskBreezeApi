from decimal import Decimal

from rest_framework import serializers
from .models import ExpenseItem, CollaboratorDetail, GroupExpense


class ExpenseItemSerializer(serializers.ModelSerializer):
    i_qty = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    i_amt = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = ExpenseItem
        fields = '__all__'
        #exclude = ["collaborator"]  # Exclude the collab_user field

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