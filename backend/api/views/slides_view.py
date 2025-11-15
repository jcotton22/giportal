from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser

from api.models import SlideModel
from api.serializers.slide_serializers import SlideModelSerializer


class SlideModelViewSet(viewsets.ModelViewSet):
    """
    CRUD + file upload for SlideModel.

    - GET /api/slides/
    - POST /api/slides/  (multipart with svs_file + question)
    - GET /api/slides/{id}/
    - etc.

    Supports filtering by question UUID:
    - GET /api/slides/?question=<question_uuid>
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SlideModelSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        qs = SlideModel.objects.all().select_related("question")
        question_id = self.request.query_params.get("question")
        if question_id:
            qs = qs.filter(question_id=question_id)
        return qs.order_by("id")
