import django_filters

from api.models import FinalModel


class FinalModelFilter(django_filters.FilterSet):
    # exact date: ?creation_date=2025-11-13
    creation_date = django_filters.DateFilter(field_name="creation_date")

    # range filters:
    # ?creation_date_after=2025-11-01
    # ?creation_date_before=2025-11-30
    creation_date_after = django_filters.DateFilter(
        field_name="creation_date",
        lookup_expr="gte",
    )
    creation_date_before = django_filters.DateFilter(
        field_name="creation_date",
        lookup_expr="lte",
    )

    # partial match on organ system name:
    # ?organ_system=gi
    organ_system = django_filters.CharFilter(
        field_name="organ_system__name",
        lookup_expr="icontains",
    )

    # "user" = uploaded_by → partial match on StaffUploader.name
    # ?uploaded_by=james
    uploaded_by = django_filters.CharFilter(
        field_name="uploaded_by__name",
        lookup_expr="icontains",
    )

    class Meta:
        model = FinalModel
        fields = [
            "creation_date",
            "organ_system",
            "uploaded_by",
            "model_type",  # still filterable by exact value: ?model_type=E
        ]
