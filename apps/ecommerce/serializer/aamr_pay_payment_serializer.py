from rest_framework import serializers

from apps.ecommerce.models import AamarPayPaymentConfirmation
from apps.users_management.serializers.basic_users_serializer import UserSerializerExtraShort


class AamarPayPaymentConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AamarPayPaymentConfirmation
        fields = "__all__"


class AamarPayPaymentConfirmationDetailsSerializer(serializers.ModelSerializer):
    created_by = UserSerializerExtraShort()
    updated_by = UserSerializerExtraShort()

    class Meta:
        model = AamarPayPaymentConfirmation
        fields = "__all__"
