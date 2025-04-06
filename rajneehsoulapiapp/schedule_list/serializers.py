from rest_framework import serializers

from rajneehsoulapiapp.schedule_list.models import ScheduleItemList, ScheduleListAttachments
from rajneehsoulapiapp.util import CustomDateTimeField

class ScheduleListAttachmentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleListAttachments
        fields = ['file']

    def to_representation(self, instance):
        return instance.file.url


class ScheduleItemListSerializers(serializers.ModelSerializer):
    dateTime = CustomDateTimeField()
    attachments = ScheduleListAttachmentUploadSerializer(many=True, read_only=True)

    class Meta:
        model = ScheduleItemList
        fields = ['id', 'dateTime', 'title', 'lastScheduleOn',
                  'isItemPinned', 'subTitle', 'isArchived',
                  'priority', 'user_id', "google_auth_user_id", "attachments"]
