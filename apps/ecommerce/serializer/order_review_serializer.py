from rest_framework import serializers

from apps.ecommerce.models import OrderAndShippingModel, ProductReviewModel
from apps.users_management.serializers.basic_users_serializer import (
    UserSerializerExtraShort,
)


class OrderAndShippingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReviewModel
        fields = "__all__"


class OrderAndShippingModelSerializerDetails(serializers.ModelSerializer):
    updated_by = UserSerializerExtraShort()
    created_by = UserSerializerExtraShort()

    class Meta:
        model = ProductReviewModel
        fields = "__all__"
