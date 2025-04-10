from django.contrib.auth.models import User
from django.db import models

from rajneehsoulapiapp.login.models import EmailIdRegistration


class ExpenseItem(models.Model):
    i_name = models.CharField(max_length=255)
    i_desp = models.TextField()
    i_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    i_notes = models.TextField()
    is_settled = models.BooleanField(default=False)
    i_amt = models.DecimalField(max_digits=10, decimal_places=2)
    date_time = models.DateTimeField()
    collaborator = models.ForeignKey(
        'CollaboratorDetail',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses'
    )  # Links the expense to a collaborator if applicable
    created_by_user = models.ForeignKey(
        EmailIdRegistration,
        on_delete=models.CASCADE,
        related_name="expense_created_by_user",
        null=True,
        blank=True
    )
    created_by_google_auth_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="expense_created_by_google_auth_user",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.i_name


from django.db import models
from django.contrib.auth.models import User
from enum import Enum


# --- Enum Definitions with .description ---
class CollaboratorStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    SETTLED = 'SETTLED', 'Settled'
    OWNED = 'OWNED', 'Owned'


class SettleMode(models.TextChoices):
    ONLINE = 'ONLINE', 'Online'
    CASH = 'CASH', 'Cash'


class OnlinePaymentsOptions(Enum):
    UPI = "UPI"
    NET_BANKING = "Net Banking"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    NEFT = "NEFT"
    RTGS = "RTGS"
    DRAFT = "Demand Draft"

    @property
    def description(self):
        return self.value


class OfflinePaymentsOptions(Enum):
    CASH = "Cash"
    BARTER = "Barter"

    @property
    def description(self):
        return self.value


# --- Combined Settle Medium Choices ---
SETTLE_MEDIUM_CHOICES = [
    (option.name, option.description)
    for option in list(OnlinePaymentsOptions) + list(OfflinePaymentsOptions)
]


# --- Model ---
class CollaboratorDetail(models.Model):

    collab_user = models.ForeignKey(
        'EmailIdRegistration',
        on_delete=models.CASCADE,
        related_name="mobile_collaborator",
        null=True,
        blank=True
    )

    collab_google_auth_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="google_collaborator",
        null=True,
        blank=True
    )

    collaborator_name = models.CharField(max_length=50, null=True, default=None)

    status = models.CharField(
        max_length=10,
        choices=CollaboratorStatus.choices,
        default=CollaboratorStatus.PENDING,
        null=True
    )

    requested_payment_qr_url = models.TextField(null=True, blank=True)  # Was URLField
    redirect_upi_url = models.TextField(null=True, blank=True)  # Was URLField

    settle_mode = models.CharField(
        max_length=10,
        choices=SettleMode.choices,
        default=SettleMode.ONLINE,
        null=True
    )

    settle_medium = models.CharField(
        max_length=20,
        choices=SETTLE_MEDIUM_CHOICES,
        default=OnlinePaymentsOptions.UPI.name,
        null=True
    )

    group_id = models.ForeignKey(
        'GroupExpense',
        on_delete=models.CASCADE,
        related_name='collaborators'
    )

    def __str__(self):
        user_info = self.collab_user or self.collab_google_auth_user
        return f"Collaborator: {user_info}, Status: {self.status}"



class GroupExpense(models.Model):
    grp_name = models.CharField(max_length=255)
    last_settled_date_time = models.DateTimeField(null=True, blank=True)  # Optional
    last_settled_amt = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    created_by_user = models.ForeignKey(
        EmailIdRegistration,
        on_delete=models.CASCADE,
        related_name="created_groups_by_mobile",
        null=True,
        blank=True
    )
    created_by_google_auth_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_groups_by_google",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.grp_name