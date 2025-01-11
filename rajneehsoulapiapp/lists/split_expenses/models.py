from django.contrib.auth.models import User
from django.db import models

from rajneehsoulapiapp.login.models import MobileRegistration


class ExpenseItem(models.Model):
    i_name = models.CharField(max_length=255)
    i_desp = models.TextField()
    i_qty = models.CharField(max_length=100)
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

    def __str__(self):
        return self.i_name


class CollaboratorDetail(models.Model):
    collab_user = models.ForeignKey(
        MobileRegistration,
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
    status = models.CharField(max_length=50, null=True, default=None)  # Status: PENDING, SETTLED, OWNED
    requested_payment_qr_url = models.URLField(null=True, blank=True)  # PayPal, gPay QR, etc.
    redirect_upi_url = models.URLField(null=True, blank=True)  # For gPay/UPI link, etc.
    settle_mode = models.CharField(max_length=50, default=None, null=True)  # Example: ONLINE, CASH
    settle_medium = models.CharField(max_length=50, default=None, null=True)  # Example: UPI, PayPal
    group_expense_id = models.ForeignKey(
        'GroupExpense',
        on_delete=models.CASCADE,
        related_name='collaborators'
    )  # Links the collaborator to the group

    def __str__(self):
        user_info = self.collab_user or self.collab_google_auth_user
        return f"Collaborator: {user_info}, Status: {self.status}"


class GroupExpense(models.Model):
    grp_name = models.CharField(max_length=255)
    t_item = models.IntegerField(default=0)  # Total items count
    t_amt = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Total amount
    last_settled_date_time = models.DateTimeField(null=True, blank=True)  # Optional
    last_settled_amt = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    created_by_user = models.ForeignKey(
        MobileRegistration,
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