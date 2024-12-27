from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rajneehsoulapiapp.views import encrypt_data, decrypt_data, compress_string_view, get_content

urlpatterns = [
    path('admin/', admin.site.urls),
    path('encrypt/', encrypt_data, name='encrypt-data'),
    path('decrypt/', decrypt_data, name='decrypt-data'),
    path('compress-string/', compress_string_view, name='compress-string'),
    path('api/content/', get_content, name='get_content'),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path("api/login/", include("rajneehsoulapiapp.login.urls")),  # Include the login package URLs
    path("api/schedule-list/", include("rajneehsoulapiapp.schedule_list.urls")),  # Include the schedule_list package URLs
    path('', include('social_django.urls', namespace='social')),
    path('api/pre/', include('rajneehsoulapiapp.before_login.urls')),  # Includes all app-level URLs
    path('api/post/', include('rajneehsoulapiapp.post_login.urls')),  # Includes all app-level URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)