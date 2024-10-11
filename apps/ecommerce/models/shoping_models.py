from django.db import models

from apps.ecommerce.models.base_models import ECommerceBaseModel
from backend.utils.text_choices import ShippingStatus


class ShoppingCartModel(ECommerceBaseModel):
    user = models.ForeignKey(
        'users_management.UserManage',
        on_delete=models.CASCADE,
        related_name='shopping_carts'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_purchased = models.BooleanField(default=False)
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)

    def __str__(self):
        return f"{self.pk} - {self.user} - {self.price} - {self.is_purchased}"


class ShoppingCartItemModel(ECommerceBaseModel):
    cart = models.ForeignKey(
        ShoppingCartModel,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    product = models.ForeignKey(
        'ecommerce.ProductsModel',
        on_delete=models.CASCADE,
        related_name='product_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.pk} - {self.cart} - {self.product} - {self.quantity} - {self.updated_at}"

    def save(self, *args, **kwargs):
        if self.cart.is_purchased:
            return
        self.price = float(self.unit_price) * self.quantity
        super().save(*args, **kwargs)

        self.cart.price = sum([item.price for item in self.cart.cart_items.all()])
        self.cart.save()


class OrderAndShippingModel(ECommerceBaseModel):
    cart = models.ForeignKey(
        ShoppingCartModel,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    shipping_address = models.TextField(null=True, blank=True)
    shipping_phone = models.CharField(max_length=15, null=True, blank=True)
    shipping_status = models.CharField(max_length=100, choices=ShippingStatus.choices, default=ShippingStatus.PENDING)


class PaymentModel(ECommerceBaseModel):
    cart = models.ForeignKey(
        ShoppingCartModel,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    payment_method = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.CharField(max_length=100, null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_info = models.JSONField(null=True, blank=True)
