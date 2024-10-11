from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.ecommerce.filters.product_filters import ProductsModelFilter
from apps.ecommerce.models import ProductsModel
from apps.ecommerce.serializer.product_serializer import (
    ProductsModelSerializer,
    ProductsModelSerializerDetails,
)
from backend.utils.custom_permission import (
    OnlyAdminCanCreateUpdateAndDeleteAnyoneCanGet,
)
from backend.utils.pagination import CustomPagination


class ProductsModelViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductsModelFilter
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [OnlyAdminCanCreateUpdateAndDeleteAnyoneCanGet]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    serializer_classes = {
        "list": ProductsModelSerializerDetails,
        "retrieve": ProductsModelSerializerDetails,
        "create": ProductsModelSerializer,
        "update": ProductsModelSerializer,
    }

    default_serializer_class = ProductsModelSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        return (
            ProductsModel.objects.select_related("updated_by", "created_by")
            .all()
            .order_by("name")
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
