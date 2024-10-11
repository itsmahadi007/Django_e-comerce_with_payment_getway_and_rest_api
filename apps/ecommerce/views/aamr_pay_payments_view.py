import datetime
import uuid

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from requests import post
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from apps.ecommerce.models import PaymentRequest, StatusChoices, AamarPayPaymentConfirmation, OrderAndShippingModel, \
    ShoppingCartModel


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def aamar_pay_payment_request(request):
    _data = request.data
    _current_date = datetime.datetime.now().strftime("%Y%m%d")  # YYYYMMDD format

    # while True:
    #     random_number = ''.join(random.choice(string.digits) for _ in range(6))  # 6 digit random number
    #     tran_id = 'VT' + current_date + random_number
    #     if not PaymentRequest.objects.filter(pg_txnid=tran_id).exists():
    #         break

    _tran_id = "DEVEXP" + _current_date + str(uuid.uuid4())[:6]

    identification_data = _data.get("identification", {})

    try:
        _cart_id = identification_data.get("cart_id")
        _cart = ShoppingCartModel.objects.get(id=_cart_id, is_purchased=False)
    except ShoppingCartModel.DoesNotExist:
        return Response(
            {"message": "Cart not found", "status": 404},
            status=404,
        )

    # print(tran_id)
    body = {
        **_data,
        'signature_key': "dbb74894e82415a2f7ff0ec3a97e4183",  # test
        "tran_id": _tran_id,
        "amount": float(_cart.price),
        'store_id': "aamarpaytest",  # test
    }
    # print("Body", body)

    url = "https://sandbox.aamarpay.com/index.php"  # test
    try:
        response = post(url, data=body)
        response_data = response.json()
        print("Response", response, " Response Data", response_data)
        if response_data == "Invalid Store ID":
            return Response(
                {"message": "Invalid Store ID", "status": 404, "data": body}, status=404
            )
        if response_data:
            PaymentRequest.objects.create(
                mer_txnid=_tran_id,
                request_by=request.user,
                all_data=body,
                cart_id=identification_data.get("cart_id"),
            )
            return Response(
                {
                    "message": "Payment request success",
                    "status": 200,
                    "data": response_data,  # test
                },
                status=200,
            )
    except Exception as error:
        print(error)
        return Response(
            {
                "message": "Payment request failed. Error is: " + str(error),
                "status": 404,
            },
            status=404,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def aamar_pay_payment_confirmation_request(request):
    _data = request.data
    # print(_data)
    with transaction.atomic():
        try:
            _payment_request_obj = PaymentRequest.objects.get(
                mer_txnid=_data.get("mer_txnid")
            )
            _payment_request_obj.status = StatusChoices.SUCCESSFUL
            _payment_request_obj.save()
        except PaymentRequest.DoesNotExist:
            return HttpResponse("Payment request/mer_txnid not found", status=404)

        _confirmation_obj = AamarPayPaymentConfirmation.objects.create(
            payment_request=_payment_request_obj,
            pay_status=_data.get("pay_status"),
            pg_txnid=_data.get("pg_txnid"),
            amount=_data.get("amount"),
            mer_txnid=_data.get("mer_txnid"),
            merchant_id=_data.get("merchant_id"),
            store_id=_data.get("store_id"),
            currency=_data.get("currency"),
            currency_merchant=_data.get("currency_merchant"),
            conversion_rate=_data.get("conversion_rate"),
            store_amount=_data.get("store_amount"),
            pay_time=_data.get("pay_time"),
            bank_txn=_data.get("bank_txn"),
            card_number=_data.get("card_number"),
            card_holder=_data.get("card_holder"),
            card_type=_data.get("card_type"),
            opt_a=_data.get("opt_a"),
            opt_b=_data.get("opt_b"),
            opt_c=_data.get("opt_c"),
            opt_d=_data.get("opt_d"),
            ip_address=_data.get("ip_address"),
            reason=_data.get("reason"),
            other_currency=_data.get("other_currency"),
            success_url=_data.get("success_url"),
            fail_url=_data.get("fail_url"),
            pg_service_charge_bdt=_data.get("pg_service_charge_bdt"),
            pg_service_charge_usd=_data.get("pg_service_charge_usd"),
            pg_card_bank_name=_data.get("pg_card_bank_name"),
            pg_card_bank_country=_data.get("pg_card_bank_country"),
            risk_level=_data.get("risk_level"),
            pg_error_code_details=_data.get("pg_error_code_details"),
            all_data=_data,
        )

        OrderAndShippingModel.objects.create(
            cart=_payment_request_obj.cart,
            created_by=_payment_request_obj.request_by,
            updated_by=_payment_request_obj.request_by,
        )
        _payment_request_obj.cart.is_purchased = True
        _payment_request_obj.cart.save()

        context = {
            "title": "Payment Confirmation",
            "cus_name": _confirmation_obj.all_data["cus_name"],
            "cus_email": _confirmation_obj.all_data[
                "cus_email"
            ],  # add the real field if you have it
            "cus_phone": _confirmation_obj.all_data[
                "cus_phone"
            ],  # add the real field if you have it
            "pay_status": _confirmation_obj.pay_status,
            "amount": _confirmation_obj.amount,
            "currency": _confirmation_obj.currency,
            "pay_time": _confirmation_obj.pay_time,
            "transactionId": _confirmation_obj.pg_txnid,
            "mer_txnid": _confirmation_obj.mer_txnid,
            # add other placeholders here
        }

        try:
            from apps.ecommerce.utils.generate_receipt import generate_receipt_for_cart
            generate_receipt_for_cart(_confirmation_obj, context)
        except Exception as error:
            print("Error in generating receipt", error)

        # return HttpResponse(html_content)
        return render(request, "PaymentSuccessPage.html", context)


@api_view(["POST"])
@permission_classes([AllowAny])
def aamar_pay_payment_confirmation_fail_request(request):
    _data = request.data
    print(_data)
    with transaction.atomic():
        try:
            _payment_request_obj = PaymentRequest.objects.get(
                mer_txnid=_data.get("mer_txnid")
            )
            _payment_request_obj.status = StatusChoices.FAILED
            _payment_request_obj.save()
        except PaymentRequest.DoesNotExist:
            return HttpResponse("Payment request/mer_txnid not found", status=404)

        confirmation_obj = AamarPayPaymentConfirmation.objects.create(
            payment_request=_payment_request_obj,
            pay_status=_data.get("pay_status"),
            pg_txnid=_data.get("pg_txnid"),
            amount=_data.get("amount"),
            mer_txnid=_data.get("mer_txnid"),
            merchant_id=_data.get("merchant_id"),
            store_id=_data.get("store_id"),
            currency=_data.get("currency"),
            currency_merchant=_data.get("currency_merchant"),
            conversion_rate=_data.get("conversion_rate"),
            store_amount=_data.get("store_amount"),
            pay_time=_data.get("pay_time")[0] or None
            if _data.get("pay_time")
            else None,
            bank_txn=_data.get("bank_txn"),
            card_number=_data.get("card_number"),
            card_holder=_data.get("card_holder"),
            card_type=_data.get("card_type"),
            opt_a=_data.get("opt_a"),
            opt_b=_data.get("opt_b"),
            opt_c=_data.get("opt_c"),
            opt_d=_data.get("opt_d"),
            ip_address=_data.get("ip_address"),
            reason=_data.get("reason"),
            other_currency=_data.get("other_currency"),
            success_url=_data.get("success_url"),
            fail_url=_data.get("fail_url"),
            pg_service_charge_bdt=_data.get("pg_service_charge_bdt"),
            pg_service_charge_usd=_data.get("pg_service_charge_usd"),
            pg_card_bank_name=_data.get("pg_card_bank_name"),
            pg_card_bank_country=_data.get("pg_card_bank_country"),
            risk_level=_data.get("risk_level"),
            pg_error_code_details=_data.get("pg_error_code_details"),
            all_data=_data,
        )

        context = {
            "title": "Payment Confirmation",
            "cus_name": confirmation_obj.all_data["cus_name"],
            "cus_email": confirmation_obj.all_data[
                "cus_email"
            ],  # add the real field if you have it
            "cus_phone": confirmation_obj.all_data[
                "cus_phone"
            ],  # add the real field if you have it
            "pay_status": confirmation_obj.pay_status,
            "amount": confirmation_obj.amount,
            "currency": confirmation_obj.currency,
            "pay_time": confirmation_obj.pay_time,
            "transactionId": confirmation_obj.pg_txnid,
            "mer_txnid": confirmation_obj.mer_txnid,
        }

        return render(request, "PaymentFaildPage.html", context)
