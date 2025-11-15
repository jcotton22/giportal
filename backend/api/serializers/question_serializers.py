# api/serializers/question_serializers.py
from rest_framework import serializers

from api.models import QuestionModel
from .slide_serializers import SlideModelSerializer


class QuestionModelSerializer(serializers.ModelSerializer):
    # related_name="files" on SlideModel.question
    files = SlideModelSerializer(many=True, read_only=True)

    class Meta:
        model = QuestionModel
        fields = (
            "question_id",
            "clinical_information",
            "question",
            "exam",   # FK to FinalModel (UUID)
            "files",  # nested slides
        )
