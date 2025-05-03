from django.db import models

from rajneehsoulapiapp.lists.split_expenses.utils.enums import CollaboratorStatus, SettleMode, SETTLE_MEDIUM_CHOICES
from rajneehsoulapiapp.login.models import EmailIdRegistration, validate_email_regex


class Group(models.Model):
    """
    Represents a group created by a registered user.
    """
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(
        EmailIdRegistration,
        related_name='group_created_by',
        on_delete=models.CASCADE
    )

    objects = models.Manager()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Group({self.id}): {self.name}"


class Collaborator(models.Model):
    """
    Represents a collaborator associated with a group. This can either be an active collaborator
    who is a registered user or a pending invitation identified by email.
    """
    createdBy = models.ForeignKey(
        EmailIdRegistration,
        related_name='collaborators_created',
        on_delete=models.CASCADE
    )
    collabUserId = models.ForeignKey(
        EmailIdRegistration,
        related_name='collaborators_user_id',
        on_delete=models.CASCADE,
        null=True
    )
    collaboratorName = models.CharField(max_length=100, default="")
    groupId = models.ForeignKey(
        Group,
        related_name='collaborators',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=False)
    collabEmailId = models.EmailField(
        max_length=45,
        validators=[validate_email_regex],
        verbose_name="Email Address"
    )

    requested_payment_qr_url = models.URLField(null=True, blank=True)

    redirect_upi_url = models.URLField(null=True, blank=True)

    status = models.CharField(
        max_length=10,
        choices=CollaboratorStatus.choices,
        default=CollaboratorStatus.PENDING
    )
    settle_modes = models.JSONField(default=list, blank=True)
    settle_mediums = models.JSONField(default=list, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Collaborator({self.id})"

from enum import Enum

class ExpenseType(Enum):
    SELF = 'self'
    SHARED_EQUALLY = 'shared-equally'
    CUSTOM_SPLIT = 'custom-split'

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name.replace('_', ' ').title()) for tag in cls]

class Expense(models.Model):
    EXPENSE_TYPE_CHOICES = [
        ('self', 'Self'),
        ('shared-equally', 'Shared Equally'),
        ('custom-split', 'Custom Split'),
    ]

    eName = models.CharField(max_length=100)
    eRawAmt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    eAmt = models.DecimalField(max_digits=10, decimal_places=2)
    eQty = models.PositiveIntegerField(default=1)
    eQtyUnit = models.CharField(max_length=100)
    eDescription = models.TextField(blank=True)
    eExpenseType = models.CharField(max_length=20, choices=ExpenseType.choices())
    eCreationId = models.CharField(max_length=6, default="0AabB9")

    addedByCollaboratorId = models.ForeignKey(
        Collaborator,
        related_name='expenses_added',
        on_delete=models.CASCADE
    )
    expenseForCollaborator = models.ForeignKey(Collaborator, on_delete=models.CASCADE, related_name='received_expenses',
                                               null=True, blank=True)
    groupId = models.ForeignKey(
        Group,
        related_name='group_expenses',
        on_delete=models.CASCADE
    )

    created_on = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.eName} - {self.eAmt} by {self.addedByCollaboratorId}"
