# Generated by Django 5.1.3 on 2025-05-03 15:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rajneehsoulapiapp', '0002_expense_erawamt_alter_authtoken_expires_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtoken',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 3, 16, 1, 40, 208576, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='expense',
            name='eAmt',
            field=models.DecimalField(decimal_places=2, max_digits=100000),
        ),
        migrations.AlterField(
            model_name='scheduleitemlist',
            name='lastScheduleOn',
            field=models.CharField(default='03-05-2025 09:29:40 PM', max_length=200),
        ),
    ]
