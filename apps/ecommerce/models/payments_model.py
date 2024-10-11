from django.db import models

from apps.users_management.models import UserManage


class StatusChoices(models.TextChoices):
    FAILED = "Failed"
    SUCCESSFUL = "Successful"
    PENDING = "Pending"


class PaymentRequest(models.Model):
    mer_txnid = models.CharField(max_length=42, unique=True)
    cart = models.ForeignKey(
        "ecommerce.ShoppingCartModel", on_delete=models.CASCADE, related_name="payments"
    )

    request_by = models.ForeignKey(
        UserManage, on_delete=models.CASCADE, related_name="payment_request"
    )
    all_data = models.JSONField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.mer_txnid} - {self.cart} - {self.status}"


class AamarPayPaymentConfirmation(models.Model):
    payment_request = models.ForeignKey(
        PaymentRequest, on_delete=models.CASCADE, related_name="payment_confirmation"
    )
    pay_status = models.CharField(max_length=10, choices=StatusChoices.choices)
    pg_txnid = models.CharField(max_length=42, unique=True)
    amount = models.FloatField(null=True, blank=True)
    mer_txnid = models.CharField(max_length=200, null=True, blank=True)
    merchant_id = models.CharField(max_length=200, null=True, blank=True)
    store_id = models.CharField(max_length=200, null=True, blank=True)
    currency = models.CharField(max_length=50, default="BDT")
    currency_merchant = models.CharField(max_length=50, null=True, blank=True)
    conversion_rate = models.FloatField(null=True, blank=True)
    store_amount = models.FloatField(null=True, blank=True)
    pay_time = models.DateTimeField(null=True, blank=True)
    bank_txn = models.CharField(max_length=20, null=True, blank=True)
    card_number = models.CharField(max_length=30, null=True, blank=True)
    card_holder = models.CharField(max_length=100, null=True, blank=True)
    card_type = models.CharField(max_length=20, null=True, blank=True)
    opt_a = models.CharField(max_length=200, null=True, blank=True)
    opt_b = models.CharField(max_length=200, null=True, blank=True)
    opt_c = models.CharField(max_length=200, null=True, blank=True)
    opt_d = models.CharField(max_length=200, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    other_currency = models.CharField(max_length=10, null=True, blank=True)
    success_url = models.URLField(max_length=200, null=True, blank=True)
    fail_url = models.URLField(max_length=200, null=True, blank=True)
    pg_service_charge_bdt = models.CharField(max_length=200, null=True, blank=True)
    pg_service_charge_usd = models.CharField(max_length=200, null=True, blank=True)
    pg_card_bank_name = models.CharField(max_length=100, null=True, blank=True)
    pg_card_bank_country = models.CharField(max_length=100, null=True, blank=True)
    risk_level = models.IntegerField(
        choices=((0, "No risk"), (1, "May be risky")), default=0, null=True, blank=True
    )
    pg_error_code_details = models.TextField(null=True, blank=True)
    all_data = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        UserManage,
        on_delete=models.SET_NULL,
        related_name="aamar_pay_payment_confirmation_created_by",
        null=True,
        blank=True,
    )

    updated_by = models.ForeignKey(
        UserManage,
        on_delete=models.SET_NULL,
        related_name="aamar_pay_payment_confirmation_updated_by",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Aamar Pay Payment Confirmation"
        verbose_name_plural = "Aamar Pay Payment Confirmations"

    def __str__(self):
        return f"Cart Id: {self.payment_request.cart.id} - {self.pg_txnid} - {self.payment_request} - {self.pay_status} - {self.amount} - {self.pay_time}"
