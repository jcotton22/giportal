from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import QuestionModel
from api.serializers.question_serializers import QuestionModelSerializer


class QuestionModelViewSet(viewsets.ModelViewSet):
    """
    CRUD for QuestionModel.

    - GET /api/questions/
    - POST /api/questions/
    - GET /api/questions/{id}/
    - etc.

    Supports filtering by exam UUID:
    - GET /api/questions/?exam=<finalmodel_uuid>
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = QuestionModelSerializer

    def get_queryset(self):
        qs = QuestionModel.objects.all().prefetch_related("files")
        exam_id = self.request.query_params.get("exam")
        if exam_id:
            qs = qs.filter(exam_id=exam_id)
        return qs.order_by("question_id")
