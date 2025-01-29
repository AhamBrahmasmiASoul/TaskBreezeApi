# Generated by Django 5.1.3 on 2025-01-24 15:12

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
                ('userMobileLinked', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rajneehsoulapiapp.emailidregistration')),
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
            name='CollaboratorDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default=None, max_length=50, null=True)),
                ('requested_payment_qr_url', models.URLField(blank=True, null=True)),
                ('redirect_upi_url', models.URLField(blank=True, null=True)),
                ('settle_mode', models.CharField(default=None, max_length=50, null=True)),
                ('settle_medium', models.CharField(default=None, max_length=50, null=True)),
                ('collab_google_auth_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='google_collaborator', to=settings.AUTH_USER_MODEL)),
                ('collab_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mobile_collaborator', to='rajneehsoulapiapp.emailidregistration')),
            ],
        ),
        migrations.CreateModel(
            name='AuthToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=40, verbose_name='Key')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rajneehsoulapiapp.emailidregistration')),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('i_name', models.CharField(max_length=255)),
                ('i_desp', models.TextField()),
                ('i_qty', models.CharField(max_length=100)),
                ('i_notes', models.TextField()),
                ('is_settled', models.BooleanField(default=False)),
                ('i_amt', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_time', models.DateTimeField()),
                ('collaborator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expenses', to='rajneehsoulapiapp.collaboratordetail')),
            ],
        ),
        migrations.CreateModel(
            name='GroupExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grp_name', models.CharField(max_length=255)),
                ('t_item', models.IntegerField(default=0)),
                ('t_amt', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('last_settled_date_time', models.DateTimeField(blank=True, null=True)),
                ('last_settled_amt', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_by_google_auth_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_groups_by_google', to=settings.AUTH_USER_MODEL)),
                ('created_by_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_groups_by_mobile', to='rajneehsoulapiapp.emailidregistration')),
            ],
        ),
        migrations.AddField(
            model_name='collaboratordetail',
            name='group_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collaborators', to='rajneehsoulapiapp.groupexpense'),
        ),
        migrations.CreateModel(
            name='ScheduleItemList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField()),
                ('title', models.CharField(default='Title', max_length=1000)),
                ('isItemPinned', models.BooleanField(default=False)),
                ('lastScheduleOn', models.CharField(default='24-01-2025 08:42:17 PM', max_length=200)),
                ('attachedImage', models.ImageField(blank=True, upload_to='images/')),
                ('subTitle', models.CharField(default='Sub Title', max_length=1000)),
                ('isArchived', models.BooleanField(default=False)),
                ('priority', models.IntegerField(default=0)),
                ('google_auth_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='google_auth_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='rajneehsoulapiapp.emailidregistration')),
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
