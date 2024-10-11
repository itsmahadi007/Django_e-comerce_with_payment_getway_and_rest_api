from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ecommerce.models import ShoppingCartModel, ShoppingCartItemModel
from apps.ecommerce.serializer.product_cart_serializer import (
    ShoppingCartModelSerializerDetails,
    ShoppingCartItemModelSerializer,
)


class ProductCartsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        carts = ShoppingCartModel.objects.filter(
            user=user, is_purchased=False
        ).prefetch_related(
            "cart_items",
            "cart_items__created_by",
            "cart_items__updated_by",
            "cart_items__product",
        )
        if not carts.exists():
            carts = ShoppingCartModel.objects.create(user=user)
        serializer = ShoppingCartModelSerializerDetails(carts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        cart = (
            ShoppingCartModel.objects.filter(user=user, is_purchased=False)
            .prefetch_related("cart_items")
            .first()
        )
        if not cart:
            cart = ShoppingCartModel.objects.create(user=user)

        serializer = ShoppingCartItemModelSerializer(data=request.data)
        with transaction.atomic():
            if serializer.is_valid():
                item = serializer.save(cart=cart, created_by=user, updated_by=user)
                self.update_item_price(item)
                self.update_cart_price(cart)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user = request.user
        item = get_object_or_404(
            ShoppingCartItemModel, pk=pk, cart__user=user, cart__is_purchased=False
        )
        serializer = ShoppingCartItemModelSerializer(
            item, data=request.data, partial=True
        )
        with transaction.atomic():
            if serializer.is_valid():
                item = serializer.save(updated_by=user)
                self.update_item_price(item)
                self.update_cart_price(item.cart)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        user = request.user
        item = get_object_or_404(
            ShoppingCartItemModel, pk=pk, cart__user=user, cart__is_purchased=False
        )
        serializer = ShoppingCartItemModelSerializer(item, data=request.data)
        with transaction.atomic():
            if serializer.is_valid():
                item = serializer.save(updated_by=user)
                self.update_item_price(item)
                self.update_cart_price(item.cart)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = request.user
        item = get_object_or_404(
            ShoppingCartItemModel, pk=pk, cart__user=user, cart__is_purchased=False
        )
        cart = item.cart
        with transaction.atomic():
            item.delete()
            self.update_cart_price(cart)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update_item_price(self, item):
        item.price = Decimal(item.unit_price) * item.quantity
        item.save()

    def update_cart_price(self, cart):
        cart.price = sum([item.price for item in cart.cart_items.all()])
        cart.save()
