from django.contrib import admin
from django.utils.timezone import localtime

from rajneehsoulapiapp.before_login.models import *
from rajneehsoulapiapp.login.models import CustomUser, AuthToken, CustomUserProfile, IST
from rajneehsoulapiapp.models import Content
from rajneehsoulapiapp.schedule_list.models import ScheduleItemList, ItemType, ScheduleListAttachments
from .address.models import Address
from .communication.models import OtpConfig
from .lists.split_expenses.models import *
from .post_login.models import *


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'sub_title', 'description', 'date_time', 'image', "imageViaUrl"]


class UserTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'access_token', 'refresh_token')  # Fields to display
    search_fields = ('user__username', 'user__email')  # Search by user username or email
    list_filter = ('created_at',)  # Filter by created_at field


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'emailIdLinked_id']


@admin.register(EmailIdRegistration)
class EmailIdRegistrationAdmin(admin.ModelAdmin):
    list_display = (['id', 'emailId', 'otpTimeStamp', 'otp', 'fcmToken'])


@admin.register(AuthToken)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'expires_at_ist', 'user']

    def expires_at_ist(self, obj):
        """Convert expires_at to IST before displaying in Django Admin."""
        return localtime(obj.expires_at, IST).strftime('%Y-%m-%d %H:%M:%S')

    expires_at_ist.admin_order_field = 'expires_at'  # Allows sorting
    expires_at_ist.short_description = 'Expires At (IST)'  # Custom column name


@admin.register(ScheduleItemList)
class ScheduleItemListAdmin(admin.ModelAdmin):
    list_display = ['id', 'dateTime', 'title', 'lastScheduleOn', 'isItemPinned', 'subTitle', 'isArchived', 'priority', 'user_id', 'google_auth_user_id']


@admin.register(CustomUserProfile)
class CustomUserProfileAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = [
        'id',
        'get_username',  # Custom method for username
        'get_password',  # Custom method for password
        'get_first_name',  # Custom method for first name
        'get_last_name',  # Custom method for last name
        'get_email',  # Custom method for email
        'phone_number',
        'is_premium_user',
        'date_joined',
        'last_updated',
    ]

    # Custom methods to fetch related User model fields
    @admin.display(description='Username')
    def get_username(self, obj):
        return obj.user.username

    @admin.display(description='Password')
    def get_password(self, obj):
        return obj.user.password

    @admin.display(description='First Name')
    def get_first_name(self, obj):
        return obj.user.first_name

    @admin.display(description='Last Name')
    def get_last_name(self, obj):
        return obj.user.last_name

    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.email


    # Fields to filter by in the admin interface
    list_filter = [
        'is_premium_user',
        'date_joined',
        'last_updated'
    ]

    # Fields to search for in the admin interface
    search_fields = [
        'user__username',  # Search by the related User model's username
        'user__email',  # Search by the related User model's email
        'phone_number',
        'user__first_name',
        'user__last_name'
    ]

    # Customize the form fields displayed in the detail view
    fields = (
        ('user', 'profile_picture'),  # Display user and profile picture in one row
        ('phone_number', 'address'),  # Display phone number and address in one row
        ('date_of_birth', 'is_premium_user'),  # Display date of birth and premium status in one row
        'bio',  # Bio field in a new row
        ('date_joined', 'last_updated')  # Display date joined and last updated in one row
    )

    # Fields that are read-only in the admin detail view
    readonly_fields = ['date_joined', 'last_updated']

    # Number of entries to display per page in the list view
    list_per_page = 20


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

from django.contrib import admin

@admin.register(AppSpecificDetails)
class AppSpecificDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'language_code', 'theme')

@admin.register(AppUpdateInfo)
class AppUpdateInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'redirect_url', 'current_version', 'update_mode')

@admin.register(AppTourInfo)
class AppTourInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subtitle', 'image')

@admin.register(AppDetails)
class AppDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'app_specific_details', 'app_update_info')
    filter_horizontal = ('app_tour_info',)

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')

from django.contrib import admin

# Inline for BottomNavOption
class BottomNavOptionInline(admin.TabularInline):
    model = BottomNavOption
    extra = 1  # Number of extra empty forms in the admin panel

# Inline for WeatherNotification
class WeatherNotificationInline(admin.TabularInline):
    model = WeatherNotification
    extra = 1  # Number of extra empty forms in the admin panel

# Admin for AppData
@admin.register(PostLoginAppData)
class PostLoginAppDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'bottom_nav_option', 'weather_notification']

# Optional: Register the related models if needed
@admin.register(BottomNavOption)
class BottomNavOptionAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'is_default_selected', 'icon_url', 'is_allowed', 'is_disabled']
    search_fields = ['title']

@admin.register(WeatherNotification)
class WeatherNotificationAdmin(admin.ModelAdmin):
    list_display = ['info']
    search_fields = ['info']


class GroupExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'grp_name',
        'last_settled_date_time',
        'created_by_user',
        'created_by_google_auth_user',
    )


class CollaboratorDetailAdmin(admin.ModelAdmin):
    list_display = ('collaborator_name', 'collab_user', 'collab_google_auth_user', 'status', 'group_id')
    list_filter = ('status', 'group_id')
    search_fields = (
        'collab_user__mobile_number',
        'collab_google_auth_user__username',
        'group__grp_name',
        'settle_mode', 'settle_medium',
    )


@admin.register(OtpConfig)
class OtpConfigAdmin(admin.ModelAdmin):
    list_display = (("via_mail",))


@admin.register(ScheduleListAttachments)
class ScheduleListAttachmentsAdmin(admin.ModelAdmin):
    list_display = ["file", "user"]

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_on')
    search_fields = ('name',)
    list_filter = ('created_on',)

@admin.register(Collaborator)
class CollaboratorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'groupId',
        'createdBy',
        'collabUserId',
        'collaboratorName',
        'created_on',
        'isActive',
        'collabEmailId',
        'status',
        'settle_modes',
        'settle_mediums',
        'requested_payment_qr_url',
        'redirect_upi_url',
    )
    list_filter = (
        'groupId',
        'createdBy',
        'status',
        'settle_modes',
        'settle_mediums',
        'isActive',
    )

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'groupId',
        'addedByCollaboratorId',
        'expenseForCollaborator',
        'eExpenseType',
        'eAmt',
        'eName',
        'created_on',
        'eCreationId'
    )
    list_filter = ('eExpenseType', 'groupId', 'created_on', 'eCreationId')
    search_fields = ('description', 'amount')
    ordering = ('-created_on',)

class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'pincode', 'address', 'user')
    search_fields = ('pincode', 'address', 'user__emailId')  # Adjust to match your user model field for search
    list_filter = ('user',)  # Filter by user in the admin interface

admin.site.register(Address, AddressAdmin)
