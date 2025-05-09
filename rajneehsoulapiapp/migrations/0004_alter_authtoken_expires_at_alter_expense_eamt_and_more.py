# Generated by Django 5.1.3 on 2025-05-03 22:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rajneehsoulapiapp', '0003_alter_authtoken_expires_at_alter_expense_eamt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtoken',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 3, 22, 46, 54, 2234, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='expense',
            name='eAmt',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='scheduleitemlist',
            name='lastScheduleOn',
            field=models.CharField(default='04-05-2025 04:14:54 AM', max_length=200),
        ),
    ]
