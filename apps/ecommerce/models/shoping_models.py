from django.db import models

from apps.ecommerce.models.base_models import ECommerceBaseModel
from backend.utils.text_choices import ShippingStatus


class ShoppingCartModel(ECommerceBaseModel):
    user = models.ForeignKey(
        "users_management.UserManage",
        on_delete=models.CASCADE,
        related_name="shopping_carts",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_purchased = models.BooleanField(default=False)
    receipt = models.FileField(upload_to="receipts/", null=True, blank=True)

    def __str__(self):
        return f"{self.pk} - {self.user} - {self.price} - {self.is_purchased}"


class ShoppingCartItemModel(ECommerceBaseModel):
    cart = models.ForeignKey(
        ShoppingCartModel, on_delete=models.CASCADE, related_name="cart_items"
    )
    product = models.ForeignKey(
        "ecommerce.ProductsModel",
        on_delete=models.CASCADE,
        related_name="product_items",
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return (f"{self.pk} - {self.cart} - {self.product} - "
                f"{self.quantity} - {self.updated_at}")



class OrderAndShippingModel(ECommerceBaseModel):
    cart = models.ForeignKey(
        ShoppingCartModel, on_delete=models.CASCADE, related_name="orders"
    )
    shipping_address = models.TextField(null=True, blank=True)
    shipping_phone = models.CharField(max_length=15, null=True, blank=True)
    shipping_status = models.CharField(
        max_length=100, choices=ShippingStatus.choices, default=ShippingStatus.PENDING
    )

    def __str__(self):
        return f"PK:{self.pk} - Cart ID:{self.cart.id} - {self.shipping_status}"


class ProductReviewModel(ECommerceBaseModel):
    cart_item = models.ForeignKey(
        ShoppingCartItemModel,
        on_delete=models.CASCADE,
        related_name="cart_item_reviews",
    )
    review = models.TextField()
    rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.pk} - {self.cart_item.product} - {self.cart_item.cart.user} - {self.rating}"