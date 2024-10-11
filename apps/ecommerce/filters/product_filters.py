from datetime import datetime

from django_filters import rest_framework as filters

from apps.ecommerce.models import ProductsModel


class ProductsModelFilter(filters.FilterSet):
    name = filters.CharFilter(method="filter")
    date_range = filters.CharFilter(method="filter")

    class Meta:
        model = ProductsModel
        fields = ["id", "name", "date_range"]

    @staticmethod
    def filter(queryset, name, value):
        if name == "name":
            return queryset.filter(name__icontains=value)
        elif name == "date_range":
            start_date_str, end_date_str = [s.strip() for s in value.split(",")]
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            data = queryset.filter(updated_at__range=(start_date, end_date))
            return data
        else:
            return queryset
