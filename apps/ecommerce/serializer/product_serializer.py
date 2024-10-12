from rest_framework import serializers

from apps.ecommerce.models import ProductsModel, ShoppingCartItemModel, ProductReviewModel
from apps.users_management.serializers.basic_users_serializer import (
    UserSerializerExtraShort,
)
from backend.utils.custom_attachchment_serializer import add_attachment_data


class ProductsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsModel
        fields = "__all__"


class ProductsModelSerializerDetails(serializers.ModelSerializer):
    updated_by = UserSerializerExtraShort()
    created_by = UserSerializerExtraShort()

    class Meta:
        model = ProductsModel
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation = add_attachment_data(representation, instance, "image")
        representation = add_attachment_data(
            representation, instance, "image_thumbnail"
        )
        return representation


class ProductsModelSerializerDetailsWithReview(serializers.ModelSerializer):
    updated_by = UserSerializerExtraShort()
    created_by = UserSerializerExtraShort()

    class Meta:
        model = ProductsModel
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation = add_attachment_data(representation, instance, "image")
        representation = add_attachment_data(
            representation, instance, "image_thumbnail"
        )

        reviews = ProductReviewModel.objects.filter(
            cart_item__product=instance
        )
        if reviews.exists():
            representation["reviews"] = [
                {
                    "cart_item": review.id,
                    "review": review.review,
                    "rating": review.rating,
                    "created_by": review.created_by.id,
                    "updated_by": review.updated_by.id,
                }
                for review in reviews
            ]


        return representation
