# Generated by Django 5.1.3 on 2025-04-10 06:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rajneehsoulapiapp', '0009_alter_authtoken_expires_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtoken',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 4, 10, 6, 37, 57, 654097, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='collaboratordetail',
            name='redirect_upi_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='collaboratordetail',
            name='requested_payment_qr_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='collaboratordetail',
            name='settle_medium',
            field=models.CharField(choices=[('UPI', 'UPI'), ('NET_BANKING', 'Net Banking'), ('CREDIT_CARD', 'Credit Card'), ('DEBIT_CARD', 'Debit Card'), ('NEFT', 'NEFT'), ('RTGS', 'RTGS'), ('DRAFT', 'Demand Draft'), ('CASH', 'Cash'), ('BARTER', 'Barter')], default='UPI', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='collaboratordetail',
            name='settle_mode',
            field=models.CharField(choices=[('ONLINE', 'Online'), ('CASH', 'Cash')], default='ONLINE', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='collaboratordetail',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('SETTLED', 'Settled'), ('OWNED', 'Owned')], default='PENDING', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='scheduleitemlist',
            name='lastScheduleOn',
            field=models.CharField(default='10-04-2025 12:05:57 PM', max_length=200),
        ),
    ]
