
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import OrganSystem, StaffUploader
from api.serializers.lookup_serializers import (
    OrganSystemSerializer,
    StaffUploaderSerializer,
)


class OrganSystemViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    """
    List/create OrganSystem lookups.

    - GET /api/organ-systems/
    - POST /api/organ-systems/
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrganSystemSerializer
    queryset = OrganSystem.objects.all().order_by("name")


class StaffUploaderViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    """
    List/create StaffUploader lookups.

    - GET /api/staff-uploaders/
    - POST /api/staff-uploaders/
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = StaffUploaderSerializer
    queryset = StaffUploader.objects.all().order_by("name")
