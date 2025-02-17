# Generated by Django 5.1.3 on 2025-02-17 00:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rajneehsoulapiapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtpConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config_key', models.CharField(max_length=255, unique=True)),
                ('config_value', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='authtoken',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 17, 0, 33, 34, 362259, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='scheduleitemlist',
            name='lastScheduleOn',
            field=models.CharField(default='17-02-2025 06:01:34 AM', max_length=200),
        ),
    ]
