from rest_framework import serializers
from .models import Image360
from django.conf import settings


class Image360Serializer(serializers.ModelSerializer):
    image360url = serializers.SerializerMethodField('get_image360url')

    class Meta:
        model = Image360
        fields = ['vendor_code', 'image360url']

    def get_image360url(self, obj):
        # return self.context['request'].build_absolute_uri(settings.MEDIA_URL + obj.iframe.name)
        return f'{settings.MY_HOST}{settings.MEDIA_URL}{obj.iframe.name}'
