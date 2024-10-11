from rest_framework import serializers

from apps.ecommerce.models import ShoppingCartModel, ShoppingCartItemModel
from apps.ecommerce.serializer.product_serializer import ProductsModelSerializerDetails


class ShoppingCartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartModel
        fields = "__all__"


class ShoppingCartItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartItemModel
        fields = "__all__"


class ShoppingCartItemModelSerializerDetails(serializers.ModelSerializer):
    product = ProductsModelSerializerDetails()

    class Meta:
        model = ShoppingCartItemModel
        fields = "__all__"


class ShoppingCartModelSerializerDetails(serializers.ModelSerializer):
    cart_items = ShoppingCartItemModelSerializerDetails(many=True)

    class Meta:
        model = ShoppingCartModel
        fields = "__all__"
