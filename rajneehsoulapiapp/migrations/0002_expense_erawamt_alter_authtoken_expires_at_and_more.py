# Generated by Django 5.1.3 on 2025-05-03 05:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rajneehsoulapiapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='eRawAmt',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='authtoken',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 3, 5, 54, 18, 969157, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='scheduleitemlist',
            name='lastScheduleOn',
            field=models.CharField(default='03-05-2025 11:22:18 AM', max_length=200),
        ),
    ]
