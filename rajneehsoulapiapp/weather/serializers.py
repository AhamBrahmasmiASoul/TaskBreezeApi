import json

from rest_framework import serializers
from .models import WeatherForecast, WeatherPincodeMappedData
from ..schedule_list.models import ScheduleItemList
from ..schedule_list.serializers import ScheduleItemListSerializers


class WeatherForecastSerializer(serializers.ModelSerializer):
    scheduleItem = ScheduleItemListSerializers(read_only=True)
    class Meta:
        model = WeatherForecast
        fields = '__all__'

    def create(self, validated_data):
        raw_schedule_item_data = self.initial_data.get('scheduleItem')
        print(f"schedule_item_data: {raw_schedule_item_data}")

        if raw_schedule_item_data:
            try:
                schedule_item_data = json.loads(raw_schedule_item_data)
                schedule_item_id = schedule_item_data.get('id')  # now it's safe
                if schedule_item_id:
                    try:
                        validated_data['scheduleItem'] = ScheduleItemList.objects.get(id=schedule_item_id)
                    except ScheduleItemList.DoesNotExist:
                        raise serializers.ValidationError(
                            {"scheduleItem": "ScheduleItemList with this ID does not exist."})
            except json.JSONDecodeError:
                raise serializers.ValidationError({"scheduleItem": "Invalid scheduleItem format."})

        return WeatherForecast.objects.create(**validated_data)


class WeatherPincodeMappedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherPincodeMappedData
        fields = '__all__'

    def validate_pincode(self, value):
        if WeatherPincodeMappedData.objects.filter(pincode=value).exists():
            raise serializers.ValidationError("This pincode already exists.")
        return value

