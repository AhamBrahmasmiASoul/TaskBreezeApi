from decimal import Decimal

from rest_framework import serializers
from .models import ExpenseItem, CollaboratorDetail, GroupExpense, SettleMode, OfflinePaymentsOptions, \
    OnlinePaymentsOptions


class ExpenseItemSerializer(serializers.ModelSerializer):
    i_qty = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    i_amt = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = ExpenseItem
        fields = '__all__'
        #exclude = ["collaborator"]  # Exclude the collab_user field

class CollaboratorDetailSerializer(serializers.ModelSerializer):
    expenses = ExpenseItemSerializer(many=True, read_only=True)  # Existing related field

    class Meta:
        model = CollaboratorDetail
        fields = '__all__'

    def validate(self, data):
        settle_mode = data.get('settle_mode')
        settle_medium = data.get('settle_medium')

        if settle_mode and settle_medium:
            # ✅ ONLINE mode can't have offline mediums
            if settle_mode == SettleMode.ONLINE:
                if settle_medium in [opt.name for opt in OfflinePaymentsOptions]:
                    raise serializers.ValidationError({
                        'settle_medium': f"Invalid medium '{settle_medium}' for ONLINE settle_mode."
                    })

            # ✅ CASH mode can't have online mediums
            elif settle_mode == SettleMode.CASH:
                if settle_medium in [opt.name for opt in OnlinePaymentsOptions]:
                    raise serializers.ValidationError({
                        'settle_medium': f"Invalid medium '{settle_medium}' for CASH settle_mode."
                    })

        return data


class GroupExpenseSerializer(serializers.ModelSerializer):
    collaborators = CollaboratorDetailSerializer(many=True, read_only=True)  # Fetch related collaborators

    class Meta:
        model = GroupExpense
        fields = '__all__'