# Generated by Django 5.1.3 on 2025-05-03 05:02

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import rajneehsoulapiapp.login.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppSpecificDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.IntegerField(default=0)),
                ('theme', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='AppTourInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('subtitle', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AppUpdateInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redirect_url', models.URLField(blank=True, null=True)),
                ('current_version', models.CharField(blank=True, max_length=50, null=True)),
                ('update_mode', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BottomNavOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('subtitle', models.CharField(blank=True, max_length=255, null=True)),
                ('is_default_selected', models.BooleanField(default=False)),
                ('icon_url', models.URLField(blank=True, null=True)),
                ('is_allowed', models.BooleanField(default=False)),
                ('is_disabled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('sub_title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('date_time', models.DateTimeField()),
                ('image', models.TextField(blank=True)),
                ('imageViaUrl', models.ImageField(blank=True, upload_to='images/')),
                ('subTitle', models.CharField(default='Sub Title', max_length=1000)),
                ('isArchived', models.BooleanField(default=False)),
                ('priority', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='EmailIdRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailId', models.EmailField(max_length=45, validators=[rajneehsoulapiapp.login.models.validate_email_regex], verbose_name='Email Address')),
                ('otpTimeStamp', models.CharField(default='', max_length=100)),
                ('otp', models.CharField(default='', max_length=100)),
                ('fcmToken', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'PENDING'), ('approved', 'APPROVED'), ('rejected', 'REJECTED')], default='pending', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='OtpConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('via_mail', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AppDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_specific_details', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='app_details', to='rajneehsoulapiapp.appspecificdetails')),
                ('app_tour_info', models.ManyToManyField(related_name='app_details', to='rajneehsoulapiapp.apptourinfo')),
                ('app_update_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='app_details', to='rajneehsoulapiapp.appupdateinfo')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('additional_info', models.CharField(blank=True, max_length=255, null=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('is_premium_user', models.BooleanField(default=False)),
                ('bio', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='customuser_set', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='customuser_set', to='auth.permission', verbose_name='user permissions')),
                ('emailIdLinked', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rajneehsoulapiapp.emailidregistration')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Collaborator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collaboratorName', models.CharField(default='', max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('isActive', models.BooleanField(default=False)),
                ('collabEmailId', models.EmailField(max_length=45, validators=[rajneehsoulapiapp.login.models.validate_email_regex], verbose_name='Email Address')),
                ('requested_payment_qr_url', models.URLField(blank=True, null=True)),
                ('redirect_upi_url', models.URLField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('SETTLED', 'Settled'), ('OWNED', 'Owned')], default='PENDING', max_length=10)),
                ('settle_modes', models.JSONField(blank=True, default=list)),
                ('settle_mediums', models.JSONField(blank=True, default=list)),
                ('collabUserId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='collaborators_user_id', to='rajneehsoulapiapp.emailidregistration')),
                ('createdBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collaborators_created', to='rajneehsoulapiapp.emailidregistration')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='AuthToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=40, verbose_name='Key')),
                ('expires_at', models.DateTimeField(default=datetime.datetime(2025, 5, 3, 5, 4, 12, 600886, tzinfo=datetime.timezone.utc))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rajneehsoulapiapp.emailidregistration')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('createdBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_created_by', to='rajneehsoulapiapp.emailidregistration')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eName', models.CharField(max_length=100)),
                ('eAmt', models.DecimalField(decimal_places=2, max_digits=10)),
                ('eQty', models.PositiveIntegerField(default=1)),
                ('eQtyUnit', models.CharField(max_length=100)),
                ('eDescription', models.TextField(blank=True)),
                ('eExpenseType', models.CharField(choices=[('self', 'Self'), ('shared-equally', 'Shared Equally'), ('custom-split', 'Custom Split')], max_length=20)),
                ('eCreationId', models.CharField(default='0AabB9', max_length=6)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('addedByCollaboratorId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses_added', to='rajneehsoulapiapp.collaborator')),
                ('expenseForCollaborator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_expenses', to='rajneehsoulapiapp.collaborator')),
                ('groupId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_expenses', to='rajneehsoulapiapp.group')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.AddField(
            model_name='collaborator',
            name='groupId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collaborators', to='rajneehsoulapiapp.group'),
        ),
        migrations.CreateModel(
            name='ScheduleItemList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField()),
                ('title', models.CharField(default='Title', max_length=1000)),
                ('isItemPinned', models.BooleanField(default=False)),
                ('lastScheduleOn', models.CharField(default='03-05-2025 10:32:12 AM', max_length=200)),
                ('subTitle', models.CharField(default='Sub Title', max_length=1000)),
                ('isArchived', models.BooleanField(default=False)),
                ('priority', models.IntegerField(default=0)),
                ('google_auth_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='google_auth_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='rajneehsoulapiapp.emailidregistration')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleListAttachments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='schedule_list/attachments/files/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='rajneehsoulapiapp.scheduleitemlist')),
            ],
        ),
        migrations.CreateModel(
            name='PostLoginAppData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bottom_nav_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_login_app_data', to='rajneehsoulapiapp.bottomnavoption')),
                ('weather_notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_login_app_data', to='rajneehsoulapiapp.weathernotification')),
            ],
        ),
    ]
