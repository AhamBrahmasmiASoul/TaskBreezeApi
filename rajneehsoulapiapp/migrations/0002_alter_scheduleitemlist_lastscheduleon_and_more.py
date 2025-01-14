# Generated by Django 5.1.3 on 2025-01-05 02:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rajneehsoulapiapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduleitemlist',
            name='lastScheduleOn',
            field=models.CharField(default='05-01-2025 07:58:46 AM', max_length=200),
        ),
        migrations.CreateModel(
            name='CollaboratorPaymentRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_payment_qr_url', models.URLField(blank=True, null=True)),
                ('redirect_upi_url', models.URLField(blank=True, null=True)),
                ('payment_method', models.CharField(choices=[('paypal', 'PayPal'), ('gpay', 'gPay')], max_length=100)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=50)),
                ('collaborator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_requests', to='rajneehsoulapiapp.collaboratordetail')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_requests', to='rajneehsoulapiapp.groupexpense')),
            ],
        ),
    ]
