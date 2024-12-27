from rest_framework import serializers
from .models import PostLoginAppData, BottomNavOption, WeatherNotification

# Serializer for BottomNavOption
class BottomNavOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BottomNavOption
        fields = ['id', 'title', 'subtitle', 'is_default_selected', 'icon_url', 'is_allowed', 'is_disabled']


# Serializer for WeatherNotification
class WeatherNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherNotification
        fields = ['id', 'info']


# Main Serializer for PostLoginAppData
class PostLoginAppDataSerializer(serializers.ModelSerializer):
    bottom_nav_option = BottomNavOptionSerializer()
    weather_notification = WeatherNotificationSerializer()

    class Meta:
        model = PostLoginAppData
        fields = ['id', 'bottom_nav_option', 'weather_notification']

    def create(self, validated_data):
        # Extract nested data
        bottom_nav_data = validated_data.pop('bottom_nav_option')
        weather_notification_data = validated_data.pop('weather_notification')

        # Create related instances
        bottom_nav_instance = BottomNavOption.objects.create(**bottom_nav_data)
        weather_notification_instance = WeatherNotification.objects.create(**weather_notification_data)

        # Create main instance with related data
        post_login_app_data = PostLoginAppData.objects.create(
            bottom_nav_option=bottom_nav_instance,
            weather_notification=weather_notification_instance
        )

        return post_login_app_data

    def update(self, instance, validated_data):
        # Update related BottomNavOption
        if 'bottom_nav_option' in validated_data:
            bottom_nav_data = validated_data.pop('bottom_nav_option')
            for attr, value in bottom_nav_data.items():
                setattr(instance.bottom_nav_option, attr, value)
            instance.bottom_nav_option.save()

        # Update related WeatherNotification
        if 'weather_notification' in validated_data:
            weather_notification_data = validated_data.pop('weather_notification')
            for attr, value in weather_notification_data.items():
                setattr(instance.weather_notification, attr, value)
            instance.weather_notification.save()

        # Update the main instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
