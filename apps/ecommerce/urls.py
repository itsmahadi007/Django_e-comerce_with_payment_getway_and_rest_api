from django.urls import path, include
from rest_framework import routers

from apps.ecommerce.views.aamr_pay_payments_view import aamar_pay_payment_request, \
    aamar_pay_payment_confirmation_request, aamar_pay_payment_confirmation_fail_request
from apps.ecommerce.views.order_shipping_view import OrderAndShippingModelViewSet
from apps.ecommerce.views.product_in_cart_view import ProductCartsView
from apps.ecommerce.views.products_view import ProductsModelViewSet

route = routers.DefaultRouter()
route.register("products", ProductsModelViewSet, basename="products")
route.register("order_shipping", OrderAndShippingModelViewSet, basename="OrderAndShippingModelViewSet")
urlpatterns = [
    path("", include(route.urls)),
    path(
        "aamar_pay_payment_request/",
        aamar_pay_payment_request,
        name="aamar_pay_payment_request",
    ),
    path(
        "aamar_pay_payment_confirmation_request/",
        aamar_pay_payment_confirmation_request,
        name="aamar_pay_payment_confirmation_request",
    ),
    path(
        "aamar_pay_payment_confirmation_fail_request/",
        aamar_pay_payment_confirmation_fail_request,
        name="aamar_pay_payment_confirmation_fail_request",
    ),
    path(
        "product_cart/",
        ProductCartsView.as_view(),
        name="ProductCartsView",
    ),
]
