from django_filters import rest_framework as filters
from .models import PlayRecord


class PlayRecordFilter(filters.FilterSet):
    min_count = filters.NumberFilter(field_name="count", lookup_expr="gte")
    max_count = filters.NumberFilter(field_name="count", lookup_expr="lte")

    class Meta:
        model = PlayRecord
        fields = ("type",)
