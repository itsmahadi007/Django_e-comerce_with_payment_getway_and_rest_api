from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.ecommerce.filters.order_shipping_filters import OrderAndShippingModelModelFilter
from apps.ecommerce.models import OrderAndShippingModel
from apps.ecommerce.serializer.order_shipping_serializer import OrderAndShippingModelSerializer, \
    OrderAndShippingModelSerializerDetails
from backend.utils.custom_permission import (
    OnlyAdminCanCreateUpdateAndDeleteAnyoneCanGet,
)
from backend.utils.pagination import CustomPagination


class OrderAndShippingModelViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderAndShippingModelModelFilter
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [OnlyAdminCanCreateUpdateAndDeleteAnyoneCanGet]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    serializer_classes = {
        "list": OrderAndShippingModelSerializerDetails,
        "retrieve": OrderAndShippingModelSerializerDetails,
        "create": OrderAndShippingModelSerializer,
        "update": OrderAndShippingModelSerializer,
    }

    default_serializer_class = OrderAndShippingModelSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        return (
            OrderAndShippingModel.objects.select_related("updated_by", "created_by")
            .all()
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
