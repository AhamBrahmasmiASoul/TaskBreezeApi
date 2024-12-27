from rest_framework import serializers

from rajneehsoulapiapp.schedule_list.models import ScheduleItemList
from rajneehsoulapiapp.util import CustomDateTimeField


class ScheduleItemListSerializers(serializers.ModelSerializer):
    dateTime = CustomDateTimeField()

    class Meta:
        model = ScheduleItemList
        fields = ['id', 'dateTime', 'title', 'lastScheduleOn', 'isItemPinned', 'subTitle', 'isArchived', 'priority', 'attachedImage', 'user_id', "google_auth_user_id"]