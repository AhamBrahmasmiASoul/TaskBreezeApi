# app/enums.py or app/choices.py

from enum import Enum
from django.db import models


class CollaboratorStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    SETTLED = 'SETTLED', 'Settled'
    OWNED = 'OWNED', 'Owned'


class SettleMode(models.TextChoices):
    ONLINE = 'ONLINE', 'Online'
    OFFLINE = 'OFFLINE', 'Offline'


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


SETTLE_MEDIUM_CHOICES = [
    (option.name, option.description)
    for option in list(OnlinePaymentsOptions) + list(OfflinePaymentsOptions)
]
