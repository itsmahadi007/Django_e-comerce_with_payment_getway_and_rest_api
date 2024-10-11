from datetime import datetime

from django_filters import rest_framework as filters

from apps.ecommerce.models import OrderAndShippingModel


class OrderAndShippingModelModelFilter(filters.FilterSet):
    cart = filters.CharFilter(method="filter")
    user = filters.CharFilter(method="filter")
    date_range = filters.CharFilter(method="filter")

    class Meta:
        model = OrderAndShippingModel
        fields = ["id", "cart", "user", "date_range"]

    @staticmethod
    def filter(queryset, name, value):
        if name == "cart":
            return queryset.filter(cart_id=value)
        elif name == "user":
            return queryset.filter(cart__user_id=value)
        elif name == "date_range":
            start_date_str, end_date_str = [s.strip() for s in value.split(",")]
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            data = queryset.filter(update_at__range=(start_date, end_date))
            return data
        else:
            return queryset
