import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Content


class Base64ImageField(serializers.Field):
    def to_representation(self, value):
        """
        Convert the Base64 image string for representation.
        """
        if not value:
            return None
        return value

    def to_internal_value(self, data):
        """
        Decode Base64 string to raw binary.
        """
        if not data:
            return None
        try:
            _format, _img_str = data.split(';base64,')
            decoded_img = base64.b64decode(_img_str)
            return ContentFile(decoded_img, name="uploaded_image.jpg")
        except Exception as _:
            raise serializers.ValidationError("Invalid Base64 image string : ExceptionOccurred : ")

class ContentSerializer(serializers.ModelSerializer):
    image = Base64ImageField()  # Custom field for Base64
    imageViaUrl = serializers.ImageField(required=False)  # Standard ImageField

    class Meta:
        model = Content
        fields = ['id', 'title', 'description', 'date_time', 'image', 'imageViaUrl']