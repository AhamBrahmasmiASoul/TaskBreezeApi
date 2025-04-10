# Generated by Django 5.1.3 on 2025-03-31 10:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rajneehsoulapiapp', '0005_alter_authtoken_expires_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='collaboratordetail',
            name='collaborator_name',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='authtoken',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 31, 10, 30, 49, 894946, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='scheduleitemlist',
            name='lastScheduleOn',
            field=models.CharField(default='31-03-2025 03:58:49 PM', max_length=200),
        ),
    ]
