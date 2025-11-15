# api/serializers/final_serializers.py
from rest_framework import serializers

from api.models import FinalModel, OrganSystem, StaffUploader
from .question_serializers import QuestionModelSerializer
from .lookup_serializers import OrganSystemSerializer, StaffUploaderSerializer


class FinalModelSerializer(serializers.ModelSerializer):
    organ_system = OrganSystemSerializer(read_only=True)
    organ_system_id = serializers.PrimaryKeyRelatedField(
        source="organ_system",
        queryset=OrganSystem.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    uploaded_by = StaffUploaderSerializer(read_only=True)
    uploaded_by_id = serializers.PrimaryKeyRelatedField(
        source="uploaded_by",
        queryset=StaffUploader.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    questions = QuestionModelSerializer(many=True, read_only=True)

    class Meta:
        model = FinalModel
        fields = (
            "id",
            "creation_date",
            "model_type",
            "organ_system",
            "organ_system_id",
            "uploaded_by",
            "uploaded_by_id",
            "questions",
        )
        read_only_fields = ("id", "creation_date")
