# api/serializers/lookup_serializers.py
from rest_framework import serializers

from api.models import OrganSystem, StaffUploader


class OrganSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganSystem
        fields = ("id", "name")


class StaffUploaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffUploader
        fields = ("id", "name")
