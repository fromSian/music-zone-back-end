from django_filters import rest_framework as filters
from .models import PlayRecord


class PlayRecordFilter(filters.FilterSet):
    min_count = filters.NumberFilter(field_name="count", lookup_expr="gte")
    max_count = filters.NumberFilter(field_name="count", lookup_expr="lte")
    type = filters.Filter(method="filter_type")

    def filter_type(self, queryset, name, value):
        if value == "ALL":
            return queryset
        else:
            value_list = value.split(",")
            target_value_list = []
            for v in value_list:
                target_value_list.append(v.strip())
            return queryset.filter(type__in=target_value_list)

    class Meta:
        model = PlayRecord
        fields = []
