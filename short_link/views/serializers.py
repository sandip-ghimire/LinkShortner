from rest_framework import serializers
from .models import Urls


class UrlSerializer(serializers.ModelSerializer):
    short_url = serializers.CharField(required=False, read_only=True, allow_blank=True, allow_null=True)
    long_url = serializers.CharField(required=False, read_only=True, allow_blank=True, allow_null=True)

    class Meta(object):
        model = Urls
        fields = ('url', 'short_url', 'long_url')
