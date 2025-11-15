from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from api.models import FinalModel
from api.serializers.final_model_serializer import FinalModelSerializer
from api.filters import FinalModelFilter


class FinalModelViewSet(viewsets.ModelViewSet):
    """
    CRUD for FinalModel (exam / question set).

    - GET /api/finals/
    - POST /api/finals/
    - GET /api/finals/{id}/
    - PUT/PATCH/DELETE /api/finals/{id}/
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = FinalModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FinalModelFilter

    def get_queryset(self):
        # eager-load lookups + questions + slides
        return (
            FinalModel.objects
            .select_related("organ_system", "uploaded_by")
            .prefetch_related("questions__files")
            .order_by("-creation_date")
        )
