from rest_framework import serializers
from .models import AppDetails, AppSpecificDetails, AppUpdateInfo, AppTourInfo

# Serializer for AppSpecificDetails
class AppSpecificDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppSpecificDetails
        fields = ['language_code', 'theme']  # Make sure field names match model

# Serializer for AppUpdateInfo
class AppUpdateInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUpdateInfo
        fields = ['redirect_url', 'current_version', 'update_mode']  # Make sure field names match model

# Serializer for AppTourInfo
class AppTourInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppTourInfo
        fields = ['title', 'subtitle', 'image']  # Make sure field names match model

# Serializer for AppDetails with nested serializers
class AppDetailsSerializer(serializers.ModelSerializer):
    app_specific_details = AppSpecificDetailsSerializer()
    app_update_info = AppUpdateInfoSerializer()
    app_tour_info = AppTourInfoSerializer(many=True)

    class Meta:
        model = AppDetails
        fields = ['app_specific_details', 'app_update_info', 'app_tour_info']  # Ensure fields match model

    def create(self, validated_data):
        # Extract the nested data
        app_specific_data = validated_data.pop('app_specific_details')
        app_update_data = validated_data.pop('app_update_info')
        app_tour_data = validated_data.pop('app_tour_info')

        # Create related models
        app_specific_instance = AppSpecificDetails.objects.create(**app_specific_data)
        app_update_instance = AppUpdateInfo.objects.create(**app_update_data)

        # Create AppDetails instance
        app_details = AppDetails.objects.create(
            app_specific_details=app_specific_instance,
            app_update_info=app_update_instance
        )

        # Create and associate AppTourInfo instances
        for tour_data in app_tour_data:
            tour_instance = AppTourInfo.objects.create(**tour_data)
            app_details.app_tour_info.add(tour_instance)

        return app_details
